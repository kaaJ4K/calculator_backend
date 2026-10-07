from decimal import Decimal


class Parser:

    def __init__(self, expression):
        self.expression = expression.replace(" ", "")
        self.position = 0


    def current_char(self):
        if self.position < len(self.expression):
            return self.expression[self.position]

        return None


    def eat(self):
        char = self.current_char()
        self.position += 1
        return char


    def parse(self):

        result = self.parse_expression()

        if self.current_char() is not None:
            raise ValueError("Invalid expression")

        return result


    # 处理 + -
    def parse_expression(self):

        result = self.parse_term()


        while True:

            char = self.current_char()


            if char == "+":

                self.eat()

                result += self.parse_term()


            elif char == "-":

                self.eat()

                result -= self.parse_term()


            else:

                break


        return result



    # 处理 * /
    def parse_term(self):

        result = self.parse_factor()


        while True:

            char = self.current_char()


            if char == "*":

                self.eat()

                result *= self.parse_factor()



            elif char == "/":

                self.eat()

                divisor = self.parse_factor()


                if divisor == 0:

                    raise ValueError("Division by zero")


                result /= divisor



            else:

                break


        return result



    # 处理数字、括号、正负号
    def parse_factor(self):


        char = self.current_char()


        # 一元正号
        if char == "+":

            self.eat()

            return self.parse_factor()



        # 一元负号
        if char == "-":

            self.eat()

            return -self.parse_factor()



        # 括号

        if char == "(":

            self.eat()


            result = self.parse_expression()


            if self.current_char() != ")":

                raise ValueError("Missing closing parenthesis")


            self.eat()


            return result



        return self.parse_number()



    # 处理数字和小数
    def parse_number(self):

        number = ""


        dot_count = 0


        while True:


            char = self.current_char()


            if char is None:

                break



            if char.isdigit():

                number += self.eat()



            elif char == ".":

                dot_count += 1


                if dot_count > 1:

                    raise ValueError("Invalid decimal number")


                number += self.eat()


            else:

                break



        if number == "":

            raise ValueError("Invalid expression")


        return Decimal(number)



def calculate_basic(expression):

    parser = Parser(expression)

    result = parser.parse()


    # 转换方便 JSON 返回

    if result == result.to_integral():

        return int(result)


    return float(result)