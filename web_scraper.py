import pandas as pd
import requests
import json
import time
import logging
import random
import argparse
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration for API requests
CONFIG = {
    'base_url': 'https://www.swiggy.com/mapi/menu/pl',
    'lat': '29.86370',
    'lng': '77.88350',
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    },
    'timeout': 10,
    'delay_range': (0.8, 1.5)  # Random delay between requests in seconds
}

def collect_restaurant_data(restaurant_ids):
    """Collect restaurant and menu data from Swiggy's API."""
    restaurants = []
    
    for index, rest_id in tqdm(enumerate(restaurant_ids, 1), total=len(restaurant_ids), desc="Scraping restaurants"):
        try:
            # Build API URL
            params = {
                'page-type': 'REGULAR_MENU',
                'complete-menu': 'true',
                'lat': CONFIG['lat'],
                'lng': CONFIG['lng'],
                'restaurantId': rest_id
            }
            response = requests.get(CONFIG['base_url'], headers=CONFIG['headers'], params=params, timeout=CONFIG['timeout'])
            response.raise_for_status()
            data = response.json()

            # Extract restaurant details
            info = data['data']['cards'][2]['card']['card']['info']
            menu_groups = data['data']['cards'][5]['groupedCard']['cardGroupMap']['REGULAR']['cards']

            # Create restaurant record
            restaurant = {
                'restaurant_name': info.get('name', 'Unknown'),
                'location': info.get('areaName', 'Not Available'),
                'address': next((label['message'] for label in info.get('labels', []) if label.get('title') == 'Address'), 'Not Available'),
                'latitude': float(info.get('latLong', '0,0').split(',')[0]),
                'longitude': float(info.get('latLong', '0,0').split(',')[1]),
                'cuisines': info.get('cuisines', []),
                'vegetarian_only': info.get('veg', False),
                'vegan_offered': 'Vegan' in info.get('cuisines', []),
                'allergen_data': None,
                'closing_time': info.get('availability', {}).get('nextCloseTime', 'Not Available'),
                'menu': []
            }

            # Check for allergen information
            for label in info.get('labels', []):
                if 'allergen' in label.get('message', '').lower():
                    restaurant['allergen_data'] = label['message']

            # Process menu items
            for group in menu_groups:
                group_info = group.get('card', {}).get('card', {})
                if 'itemCards' in group_info:
                    category = group_info.get('title', 'General')
                    for item in group_info['itemCards']:
                        item_info = item['card']['info']
                        name = item_info.get('name', 'Unnamed Item')
                        description = item_info.get('description', '') or ''

                        # Determine spice level
                        spice_level = 'Medium'
                        desc_lower = description.lower()
                        if any(keyword in desc_lower for keyword in ['spicy', 'hot', 'fiery']):
                            spice_level = 'High'
                        elif any(keyword in desc_lower for keyword in ['mild', 'light', 'gentle']):
                            spice_level = 'Low'

                        # Create menu item
                        menu_item = {
                            'name': name,
                            'description': description,
                            'category': category,
                            'price': (item_info.get('price') or item_info.get('defaultPrice') or 0) / 100,
                            'rating': item_info.get('ratings', {}).get('aggregatedRating', {}).get('rating', None),
                            'rating_count': item_info.get('ratings', {}).get('aggregatedRating', {}).get('ratingCountV2', '0'),
                            'spice_level': spice_level,
                        }
                        restaurant['menu'].append(menu_item)

            restaurants.append(restaurant)
            logging.info(f'({index}/{len(restaurant_ids)}) Scraped: {restaurant["restaurant_name"]}')

            # Random delay to prevent rate limiting
            time.sleep(random.uniform(*CONFIG['delay_range']))

        except Exception as e:
            logging.error(f'({index}/{len(restaurant_ids)}) Error scraping restaurant ID {rest_id}: {str(e)}')
            continue

    return restaurants

def save_to_json(data, filename):
    """Write data to a JSON file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logging.info(f'Saved data to {filename}')
    except Exception as e:
        logging.error(f'Error saving {filename}: {str(e)}')

def main(args):
    """Execute the Swiggy API scraping and data cleaning pipeline."""
    # Reduced list of restaurant IDs (10 instead of 56)
    restaurant_ids = ['215512','320649','395878','403832','204036','920393','893267','804371','117228','116439'
    ]

    # Scrape restaurant data
    scraped_data = collect_restaurant_data(restaurant_ids)

    # Save raw data
    raw_output = args.output or 'swiggy_data.json'
    save_to_json(scraped_data, raw_output)

    # Load into DataFrame for cleaning
    try:
        df = pd.read_json(raw_output)
    except Exception as e:
        logging.error(f'Error loading JSON into DataFrame: {str(e)}')
        return

    # Log DataFrame structure
    logging.info('DataFrame structure:')
    logging.info(df.info())

    # Remove unnecessary columns
    try:
        df.drop(columns=['restaurant_name', 'allergen_data'], axis=1, inplace=True)
        logging.info('Removed columns: restaurant_name, allergen_data')
    except Exception as e:
        logging.error(f'Error removing columns: {str(e)}')

    # Save cleaned data
    cleaned_output = args.output.replace('.json', '_processed.json') if args.output else 'processed_swiggy_data.json'
    save_to_json(df.to_dict(orient='records'), cleaned_output)

if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Scrape Swiggy restaurant data and process it.')
    parser.add_argument('--output', type=str, help='Output JSON file name (default: swiggy_data.json)')
    args = parser.parse_args()
    main(args)