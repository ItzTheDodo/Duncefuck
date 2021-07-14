
class DataTypes:

    def parse_int(self, rep: str):
        digits = rep.split("+")
        item = 0
        for i in digits:
            item += i.count(".") * pow(10, i.count("?"))
        return int(item / 10)

    def parse_float(self, rep: str):
        sp = rep.split("||")
        return float("%s.%s" % (str(self.parse_int(sp[1])), str(self.parse_int(sp[0]))))

    def parse_char(self, rep: str):
        return chr(self.parse_int(rep))

    def string_split(self, item: str, regex: str):
        output = []
        in_p = False
        count = 0
        last = 0
        for i in item:
            if i == "|":
                in_p = not in_p
            elif i == regex and not in_p:
                output.append(item[last:count])
                last = count + 1
            count += 1
        output.append(item[last:count])
        return output

    def parse_string(self, rep: str):
        return "".join(self.parse_char(i) for i in self.string_split(rep, "+"))

    def parse_variable(self, rep: str):
        return rep.count(".")
