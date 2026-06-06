import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, InputLayer

def build_intentflow_model(input_shape=(30, 132), num_classes=2):
    """
    Builds a stacked LSTM model optimized for unrolled TFLite cross-compilation.
    """
    model = Sequential([
        InputLayer(input_shape=input_shape),
        
        # Adding unroll=True strips away platform-specific Cudnn operations
        LSTM(64, return_sequences=True, activation='tanh', unroll=True),
        Dropout(0.2),
        
        LSTM(64, return_sequences=False, activation='tanh', unroll=True),
        Dropout(0.2),
        
        Dense(32, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    
    return model
