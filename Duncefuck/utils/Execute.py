from utils.Lexer import *
from utils.Datatypes import DataTypes


class Exec:

    def __init__(self, lex: list):

        self.DATATYPES = DataTypes()
        self.VARIABLES = {}
        self.HANDLER_REG = {"assignment": self._assignment_handler, "print_statement": self._print_handler, "mathematical_operation": self._maths_handler, "comment": self._comment_handler, "if_statement": self._if_statement_handler, "item": self._item_handler, "comparision": self._comparison_handler, "while_loop": self._while_handler, "function_declare": self._function_declare_handler, "function_call": self._function_call_handler, "input": self._input_handler}
        self.FUNCTIONS = {}

        for i in lex:
            try:
                self.HANDLER_REG[i.getType()](i.getItem())
            except KeyError:
                print(i, "Invalid Type")

    def _lex_item_by_datatype(self, rep: str):
        if rep.__contains__("%"):
            return self.DATATYPES.parse_variable(rep), "var"
        elif rep.__contains__("||"):
            return self.DATATYPES.parse_float(rep), "float"
        elif rep.__contains__("|") and len(self.DATATYPES.string_split(rep, "+")) > 1:
            return self.DATATYPES.parse_string(rep), "string"
        elif rep.__contains__("|"):
            return self.DATATYPES.parse_char(rep), "char"
        else:
            return self.DATATYPES.parse_int(rep), "int"

    def _get_item_datatype(self, item):
        try:
            float(item)
            if isinstance(item, float) or str(item).__contains__("."):
                return "float", float
        except ValueError:
            pass
        try:
            int(item)
            return "int", int
        except ValueError:
            pass
        if len(str(item)) == 1:
            return "char", str
        else:
            return "string", str

    def _assignment_handler(self, line):
        var = self.DATATYPES.parse_variable(line[0].getItem())
        val = self.HANDLER_REG[line[1].getType()](line[1].getItem())
        self.VARIABLES[str(var)] = (self._get_item_datatype(val)[1](val), self._get_item_datatype(val)[0])

    def _print_handler(self, line: BlockArray):
        val = []
        for i in line:
            if i.getType() != "print_start" and i.getType() != "print_end":
                val.append(self.HANDLER_REG[i.getType()](i.getItem()))
        print(*val)

    @staticmethod
    def _parse_maths_calc(item: str):
        sp = []
        count = 0
        prev_point = 0
        for i in item:
            if i == "+" and item[count + 1] == "+":
                sp.append(item[prev_point:count])
                sp.append("add")
                prev_point = count + 2
            elif i == "-" and item[count + 1] == "-":
                sp.append(item[prev_point:count])
                sp.append("sub")
                prev_point = count + 2
            elif i == "*":
                sp.append(item[prev_point:count])
                sp.append("mul")
                prev_point = count + 1
            elif i == "/":
                sp.append(item[prev_point:count])
                sp.append("div")
                prev_point = count + 1
            count += 1
        sp.append(item[prev_point:count])
        return sp

    @staticmethod
    def _calculate_maths_item(num1, num2, op):
        if op == "sub":
            return num1 - num2
        if op == "add":
            return num1 + num2
        if op == "mul":
            return num1 * num2
        if op == "div":
            return num1 / num2

    def _maths_handler(self, line: str):
        func = ["div", "sub", "add", "mul"]
        sp = self._parse_maths_calc(line)
        count = 0
        for i in sp:
            if i not in func:
                k = list(self._lex_item_by_datatype(i))
                if k[1] == "var":
                    k[0] = self.VARIABLES.get(str(k[0]))[0]
                sp[count] = k[0]
            count += 1
        for i in func:
            count = 0
            for k in sp:
                if k == i:
                    sp[count - 1] = self._calculate_maths_item(sp[count - 1], sp[count + 1], sp[count])
                    sp.pop(count)
                    sp.pop(count)
                count += 1
        return sp[0]

    def _comment_handler(self, line: str):
        pass

    def _item_handler(self, line: str):
        it = self._lex_item_by_datatype(line)
        try:
            return self.VARIABLES[str(it[0])][0] if it[1] == "var" else it[0]
        except KeyError:
            raise Exception("Variable: %s not defined" % str(it[0]))

    def _if_statement_handler(self, line: BlockArray):
        val = False
        in_statement = False
        for i in line:
            if i.getType() == "if_end":
                in_statement = not in_statement
            if in_statement:
                val = self.HANDLER_REG[i.getType()](i.getItem())
            if i.getType() == "if_start":
                in_statement = not in_statement
        if val == "True":
            in_statement = False
            for i in line:
                if i.getType() == "if_end":
                    in_statement = not in_statement
                if i.getType() != "if_start" and i.getType() != "if_end" and not in_statement:
                    self.HANDLER_REG[i.getType()](i.getItem())
                if i.getType() == "if_start":
                    in_statement = not in_statement

    @staticmethod
    def _parse_comparison_op(item: str):
        sp = []
        count = 0
        prev_point = 0
        for i in item:
            if i == "=" and item[count + 1] == "=":
                sp.append(item[prev_point:count])
                sp.append("equal")
                prev_point = count + 2
            elif i == "!" and item[count + 1] == "=":
                sp.append(item[prev_point:count])
                sp.append("not equal")
                prev_point = count + 2
            elif i == ">" and item[count + 1] == "=":
                sp.append(item[prev_point:count])
                sp.append("less than or equal")
                prev_point = count + 2
            elif i == "<" and item[count + 1] == "=":
                sp.append(item[prev_point:count])
                sp.append("more than or equal")
                prev_point = count + 2
            elif i == ">":
                sp.append(item[prev_point:count])
                sp.append("less than")
                prev_point = count + 1
            elif i == "<":
                sp.append(item[prev_point:count])
                sp.append("more than")
                prev_point = count + 1
            count += 1
        sp.append(item[prev_point:count])
        return sp

    @staticmethod
    def _calculate_comparison_item(item1, item2, op):
        if op == "equal":
            return item1 == item2
        if op == "not equal":
            return item1 != item2
        if op == "less than or equal":
            return item1 >= item2
        if op == "more than or equal":
            return item1 <= item2
        if op == "less than":
            return item1 > item2
        if op == "more than":
            return item1 < item2

    def _comparison_handler(self, line: str):
        func = ["equal", "not equal", "less than or equal", "more than or equal", "less than", "more than"]
        sp = self._parse_comparison_op(line)
        count = 0
        for i in sp:
            if i not in func:
                k = list(self._lex_item_by_datatype(i))
                if k[1] == "var":
                    k[0] = self.VARIABLES.get(str(k[0]))[0]
                sp[count] = k[0]
            count += 1
        count = 0
        for k in sp:
            if k in func:
                sp[count - 1] = str(self._calculate_comparison_item(sp[count - 1], sp[count + 1], sp[count]))
                sp.pop(count)
                sp.pop(count)
            count += 1
        return sp[0]

    def _while_handler(self, line: BlockArray):
        val = "True"
        while val == "True":
            val = False
            in_statement = False
            for i in line:
                if i.getType() == "while_end":
                    in_statement = not in_statement
                if in_statement:
                    val = self.HANDLER_REG[i.getType()](i.getItem())
                if i.getType() == "while_start":
                    in_statement = not in_statement
            if val == "False":
                break
            in_statement = False
            for i in line:
                if i.getType() == "while_end":
                    in_statement = not in_statement
                if i.getType() != "while_start" and i.getType() != "while_end" and not in_statement:
                    self.HANDLER_REG[i.getType()](i.getItem())
                if i.getType() == "while_start":
                    in_statement = not in_statement

    def _function_declare_handler(self, line: BlockArray):
        name = ""
        for i in line:
            if i.getType() == "function_name":
                name = self._lex_item_by_datatype(i.getItem())[0]
                self.FUNCTIONS[name] = []
            elif i.getType() != "function_start" and i.getType() != "function_end":
                self.FUNCTIONS[name].append(i)

    def _function_call_handler(self, line: str):
        name = self._lex_item_by_datatype(line.replace("!", ""))[0]
        for i in self.FUNCTIONS[name]:
            self.HANDLER_REG[i.getType()](i.getItem())

    def _input_handler(self, line: str):
        it = self._lex_item_by_datatype(line)
        it = self.VARIABLES[str(it[0])][0] if it[1] == "var" else it[0]
        return input(it)
