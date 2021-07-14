

class Block:

    def __init__(self, item: str, t: str):

        self._item = item
        self._type = t

    def __repr__(self):
        return "Block(item='{}', t='{}')".format(self._item, self._type)

    def __str__(self):
        return self.__repr__()

    def getItem(self):
        return self._item

    def getType(self):
        return self._type


class BlockArray(list):

    def __init__(self, t: str, *args: Block):
        super().__init__(args)
        self._type = t

    def getItem(self):
        return self

    def getType(self):
        return self._type

    def __repr__(self):
        return "BlockArray(t={}, *args={})".format(self._type, list(self).__repr__())

    def __str__(self):
        return self.__repr__()


class Lexer:

    def __init__(self, statements: list):

        self.__st = statements
        self._lexed = BlockArray("Main")

        for i in self.__st:
            self._lexed.append(self._lex_line(i))

        self._clean()

    def _lex_line(self, item: str):
        if item[:1] == "#":
            return Block(item, "comment")
        elif item.__contains__("    "):
            self._lexed[len(self._lexed) - 1].append(self._lex_line(item.replace("    ", "")))
            self._clean()
        elif item.__contains__("{") and item.__contains__("}"):
            return BlockArray("if_statement", Block("{", "if_start"), self._lex_line(item.replace("{", "").replace("}", "")), Block("}", "if_end"))
        elif item.__contains__("-") and not item.__contains__("--"):
            return BlockArray("while_loop", Block("-", "while_start"), self._lex_line(item.replace("-", "")), Block("-", "while_end"))
        elif item.__contains__(":"):
            return BlockArray("function_declare", Block("-", "function_start"), Block(item.replace(":", ""), "function_name"), Block("-", "function_end"))
        elif item.__contains__("!"):
            return Block(item, "function_call")
        elif item.__contains__("~"):
            return BlockArray("assignment", self._lex_line(item.split("~")[0]), self._lex_line(item.split("~")[1]))
        elif item.__contains__("[") and item.__contains__("]"):
            return BlockArray("print_statement", Block("[", "print_start"), self._lex_line(item.replace("[", "").replace("]", "")), Block("]", "print_end"))
        elif item.__contains__("\""):
            return Block(item.replace("\"", ""), "input")
        elif item.__contains__("++") or item.__contains__("--") or item.__contains__("*") or item.__contains__("/"):
            return Block(item, "mathematical_operation")
        elif item.__contains__("(") and item.__contains__(")"):
            return Block(item.replace("(", "").replace(")", ""), "comparision")
        else:
            return Block(item, "item")

    def _clean(self):
        # bc people don't know how to format files *faceplam*
        self._lexed = list(filter("".__ne__, self._lexed))
        self._lexed = list(filter(None.__ne__, self._lexed))

    def _recursion_path(self, path: list, item: BlockArray):
        item = item[path[0]]
        path.pop(0)
        if len(path) > 0:
            item = self._recursion_path(path, item)
        return item

    def get_lexed_file(self):
        return self._lexed

    def get_lexed_stream(self, path: list = None):
        item = self._lexed
        if path is not None:
            item = self._recursion_path(path, item)
        for i in item:
            yield i
