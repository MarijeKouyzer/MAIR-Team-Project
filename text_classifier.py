from keras.layers import Input, Embedding, LSTM, Dense
from keras.models import Model
from keras.utils import to_categorical
from numpy import array


class TextClassifier:

    def __init__(self, vocabulary_size: int, sequence_length=100):
        # Setup the layers
        self.main_input = Input(shape=(sequence_length,),
                                dtype='int32',
                                name='main_input')
        x = Embedding(output_dim=516,
                      input_dim=vocabulary_size,
                      input_length=sequence_length,
                      mask_zero=True)(self.main_input)
        x = LSTM(32)(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        x = Dense(64, activation='relu')(x)
        self.main_output = Dense(16,
                                 activation='softmax',
                                 name='main_output')(x)
        # Initialise the model
        self.model: Model = None

    def train(self, input_list: array, output_list: array):
        self.model = Model(inputs=[self.main_input], outputs=[self.main_output])
        self.model.compile(optimizer="nadam",
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])
        self.model.fit(input_list,
                       to_categorical(output_list),
                       batch_size=64,
                       epochs=10,
                       verbose=1)

    def evaluate(self, input_list: array, output_list: array):
        return self.model.evaluate(input_list, to_categorical(output_list), verbose=1)

    def predict_speech_act(self, x_input: array):
        return self.model.predict(x_input)[0]
