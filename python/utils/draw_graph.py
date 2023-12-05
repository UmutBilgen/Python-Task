
import random


def word_graph_draw(data,header):
    """
        Generate and save a bar graph based on word frequency data.

        Parameters:
        - data: A list of tuples where each tuple contains a word and its frequency.
        - header: A header string used for naming the graph file.

        Returns:
        - None
    """
    import matplotlib.pyplot as plt
    kelimeler, sayilar = zip(*data)
    header = header.split('.com/')[1].split('/')[0]
    plt.bar(kelimeler, sayilar, color='blue')
    plt.xlabel('Kelimeler')
    plt.ylabel('Sayılar')
    plt.title('Kelime Sayısı Grafiği')
    plt.savefig(f'./images/{header}.png')
    plt.clf()
