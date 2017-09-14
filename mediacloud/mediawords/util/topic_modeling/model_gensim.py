import gensim

# from mediawords.db import connect_to_db
from mediawords.util.topic_modeling.sample_handler import SampleHandler
from mediawords.util.topic_modeling.topic_model import BaseTopicModel
from mediawords.util.topic_modeling.token_pool import TokenPool
from typing import Dict, List


class ModelGensim(BaseTopicModel):
    """Generate topics of each story based on the LDA model
    ModelGensim operates on a single story at a time
    by comparing the occurrence of each token in all sentences of that story.
    It does not consider the rest of stories. The benefits of this approach include:
    1. Each story contains the word in the topics of that story
    2. There is a fixed number of topics for each story"""

    def __init__(self) -> None:
        self._story_number = 0
        self._stories_ids = []
        self._stories_tokens = []
        self._dictionary = None
        self._corpus = []
        self._WORD_SPLITTER = ' + '
        self._COEFFICIENT_SPLITTER = '*'

    def add_stories(self, stories: Dict[int, List[List[str]]]) -> None:
        """
        Adding new stories into the model
        :param stories: a dictionary of new stories
        """
        for story in stories.items():
            story_id = story[0]
            story_tokens = story[1]
            self._stories_ids.append(story_id)
            self._stories_tokens.append(story_tokens)

        self._story_number = len(self._stories_ids)

    def summarize_topic(self, topic_number: int = 1,
                        word_number: int = 4, passes: int = 100) -> Dict[int, list]:
        """
        summarize the topic of each story based on the frequency of occurrence of each word
        :return: a dictionary of story id
        and corresponding list of TOPIC_NUMBER topics (each topic contains WORD_NUMBER words)
        """

        story_topic = {}

        for i in range(len(self._stories_ids)):
            # turn our token documents into a id <-> term dictionary
            self._dictionary = gensim.corpora.Dictionary(self._stories_tokens[i])

            # convert token documents into a document-term matrix
            self._corpus = [self._dictionary.doc2bow(text) for text in self._stories_tokens[i]]

            # generate LDA model
            self._model = gensim.models.ldamodel.LdaModel(
                corpus=self._corpus, num_topics=topic_number,
                id2word=self._dictionary, passes=passes)

            raw_topics = self._model.print_topics(num_topics=topic_number, num_words=word_number)

            story_topic[self._stories_ids[i]] = self._format_topics(raw_topics=raw_topics)

        return story_topic

    def _format_topics(self, raw_topics: List[tuple]) -> List[List[str]]:
        """
        Return topics in the desired format
        :param raw_topics: un-formatted topics
        :return: formatted topics
        """
        formatted_topics = []
        for topic in raw_topics:
            words_str = topic[1]
            # change the format
            # from 'COEFFICIENT1*"WORD1" + COEFFICIENT2*"WORD2" + COEFFICIENT3*"WORD3"'
            # to   [WORD1, WORD2, WORD3]
            words = [word_str.split(self._COEFFICIENT_SPLITTER)[1][1:-1]
                     for word_str in words_str.split(self._WORD_SPLITTER)]
            formatted_topics.append(words)

        return formatted_topics

    def evaluate(self):
        pass


# A sample output
if __name__ == '__main__':
    model = ModelGensim()

    # pool = TokenPool(connect_db())
    # model.add_stories(pool.output_tokens(1, 0))
    # model.add_stories(pool.output_tokens(5, 1))

    pool = TokenPool(SampleHandler())
    model.add_stories(pool.output_tokens())

    print(model.summarize_topic())
