""" Next symbol prediction """


class Randomness:
    """ Class for emulation AI by statistics """

    TRAIN_LIMIT = 100
    TEST_LIMIT = 4
    DATA_VALUES = '01'
    TRAIN_PROMPT = 'Print a random string containing 0 or 1:\n'
    TEST_PROMPT = 'Please enter a test string containing 0 or 1:\n'
    WARN_PROMPT = 'some wrong input\n'

    def __init__(self):
        self.training_data: str = ''
        self.prediction_data: str = ''
        self.triads: dict[str, list[int]] = {f'{t:03b}': [0, 0] for t in range(8)}
        self.balance: int = 1000

    def play(self):
        """Game process """
        print('Please provide AI some data to learn...',
              'The current data length is 0, 100 symbols left\n', sep='\n')

        self.load('train')
        self.data_process()

        print('\nYou have $1000. Every time the system successfully predicts your next press, you lose $1.',
              'Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!\n', sep='\n')

        while (inp := input(self.TRAIN_PROMPT)) != 'enough':
            if self.valid_test(inp):
                self.make_prediction()
        else:
            print('Game over!')

    def data_process(self) -> None:
        """Making triads from user's input"""
        for i in range(len(self.training_data) - 3):
            triplet, follow = self.training_data[i: i + 3], int(self.training_data[i + 3])
            self.triads[triplet][follow] += 1

    def make_prediction(self) -> None:
        """Making prediction based on user's input"""
        prediction: list[str] = []
        correct: int = 0
        total: int = len(self.prediction_data) - 3

        for idx in range(len(self.prediction_data) - 3):
            triplet = self.prediction_data[idx: idx + 3]
            zeros, ones = self.triads[triplet]
            predicted_value = self.DATA_VALUES[zeros < ones]
            prediction.append(predicted_value)
            if predicted_value == self.prediction_data[idx + 3]:
                correct += 1

        print('predictions:', ''.join(prediction))
        print(f'\nComputer guessed {correct} out of {total} symbols right ({correct / total * 100:.2f} %)')

        self.balance += total - 2 * correct
        print(f'Your balance is now ${self.balance}')

    def load(self, mode: str) -> None:
        """Data initialization
            mode: switching between train | test mode
        """

        if mode == 'train':
            self.training_data = self.read([], self.TRAIN_PROMPT, self.TRAIN_LIMIT)
            print('\nFinal data string:')
            print(self.training_data)
        elif mode == 'test':
            self.prediction_data = self.read([], self.TEST_PROMPT, self.TEST_LIMIT)
        else:
            raise ValueError('Incorrect value - please choose from [train|test]')

    def read(self, data: list[str], prompt, size):
        """Process user's input"""
        while len(data) < size:
            inp: str = input(prompt)
            data.extend(filter(self.DATA_VALUES.__contains__, inp))

            if len(data) < size:
                print(f'Current data length is {len(data)}, {size - len(data)} symbols left')

        return ''.join(data)

    def valid_test(self, inp: str) -> bool:
        """Process user's input"""
        data = list(filter(self.DATA_VALUES.__contains__, inp))

        if len(data) < len(inp) or len(data) < self.TEST_LIMIT:
            print(self.WARN_PROMPT)
            return False

        self.prediction_data = ''.join(data)
        return True


if __name__ == '__main__':
    model = Randomness()
    model.play()
