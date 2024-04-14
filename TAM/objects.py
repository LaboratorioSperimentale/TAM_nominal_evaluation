class Token:
    """
    The Token class represents a token with attributes such as token ID, form, lemma, part of speech,
    head, and dependency relation.
    """
    def __init__(self, tok_id:int, form:str, lemma:str, pos:str,
                 head: int, deprel:str) -> None:
        """
        This Python function initializes object attributes for a token with specified parameters.

        Args:
          tok_id (int): The `tok_id` parameter is used to store the token ID of
        a linguistic unit in a data structure. It is an integer value that uniquely identifies the token
        within the structure.
          form (str): The `form` parameter of the class is a string that
        represents the surface form of a token. It refers to the actual word or punctuation as
        it appears in the text.
          lemma (str): The `lemma` parameter is used to store the base form or
        dictionary form of a word. It represents the canonical form of a word, which is often used in
        linguistic analysis and natural language processing tasks.
          pos (str): POS stands for Part of Speech. It is used to store the part of speech information
        of a token.
          head (int): The `head` parameter represents the syntactic head of the
        current token in a dependency tree. It is an integer value that indicates the position of the
        head token to which the current token is syntactically related.
          deprel (str): The `deprel` parameter represents the dependency
        relation of a token in a syntactic structure. It specifies the grammatical relationship between
        the token and its head in a dependency tree. This information is crucial for understanding the
        syntactic structure of a sentence.
        """

        self.id = tok_id
        self.form = form
        self.lemma = lemma
        self.pos = pos
        self.head = head
        self.deprel = deprel


    def __repr__(self) -> str:
        """
        The `__repr__` function returns a string representation of an object's form, part of speech,
        dependency relation, and head.

        Returns:
          The `__repr__` method is returning a formatted string that includes the values of the `form`,
        `pos`, `deprel`, and `head` attributes of the object. The format of the string is
        "{form}/{pos}/{deprel}:{head}".
        """
        return f"{self.form}/{self.pos}/{self.deprel}:{self.head}"


class Sentence:
    """
    This Python class named Sentence represents a sentence by storing tokens and providing methods to
    add tokens, check if it's empty, retrieve a token by ID, and display the sentence as a string.
    """
    def __init__(self, source:str) -> None:
        """
        This Python function initializes an object with a source string, an empty list for sentences,
        and an empty dictionary for sentence mapping.

        Args:
          source (str): The identifier of the corpus from which the sentence is drawn.
        """
        self.sentence = []
        self.source = source
        self.sentence_map = {}

    def add_token(self, token:Token) -> None:
        """
        The `add_token` function appends a token to a list and maps the token's ID to the token itself.

        Args:
          token (Token): The `token` parameter is of type `Token`, which is an object representing a token
        in natural language processing tasks. The `add_token` method is designed to add a
        `Token` object to a list called `sentence` and also map the token's ID to the token object
        """
        self.sentence.append(token)
        self.sentence_map[token.id] = token

    def empty(self):
        """
        The `empty` function checks if the `sentence` attribute of an object is empty and returns `True`
        if it is, `False` otherwise.

        Returns:
          If the length of the `self.sentence` is greater than 0, then `False` is being returned.
        Otherwise, `True` is being returned.
        """
        if len(self.sentence) > 0:
            return False
        return True

    def get_token(self, tok_id:int) -> Token:
        """
        This function returns a Token object based on the provided token ID.

        Args:
          tok_id (int): The `tok_id` parameter in the `get_token` method is an integer that represents
        the unique identifier of a token. This method retrieves and returns the token object associated
        with the given `tok_id` from the `sentence_map` dictionary.

        Returns:
          The `Token` object corresponding to the `tok_id` provided is being returned.
        """
        return self.sentence_map[tok_id]

    def __repr__(self) -> str:
        """
        The `__repr__` method in the Python code snippet returns a string by joining the `form`
        attribute of each element in the `sentence` list with a space separator.

        Returns:
          The `__repr__` method is returning a string that consists of joining the `form` attribute
        of each element in the `sentence` list with a space in between.
        """
        return " ".join(x.form for x in self.sentence)