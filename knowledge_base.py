
import pandas as pd
import logging

class KnowledgeBase:
    """Manages the knowledge base for the RAG chatbot."""

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.documents = []
        self.load_data()

    def load_data(self):
        """Load and preprocess the scraped data into a list of documents."""
        try:
            df = pd.read_json(self.data_path)
            logging.info(f"Loaded data with {len(df)} restaurants")
            for _, row in df.iterrows():
                row_dict = row.to_dict()
                if isinstance(row_dict.get('closing_time'), pd.Timestamp):
                    row_dict['closing_time'] = row_dict['closing_time'].isoformat()
                doc = {
                    'title': f"{row['restaurant_name']} - Restaurant Info",
                    'text': f"Restaurant: {row['restaurant_name']}, Location: {row['location']}, Cuisines: {', '.join(row['cuisines'])}, Vegetarian: {row['vegetarian_only']}, Closing Time: {row['closing_time']}"
                }
                self.documents.append(doc)
                for item in row['menu']:
                    doc = {
                        'title': f"{item['name']} at {row['restaurant_name']}",
                        'text': f"{item['name']} at {row['restaurant_name']}: {item['description']} (Price: ₹{item['price']}, Spice: {item['spice_level']}, Category: {item['category']})"
                    }
                    self.documents.append(doc)
            logging.info(f"Processed {len(self.documents)} documents")
        except Exception as e:
            logging.error(f"Failed to load data: {str(e)}")
            raise
