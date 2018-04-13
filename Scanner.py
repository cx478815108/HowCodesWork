# -*- coding: utf-8 -*-

codeTemp = """
func test(Integer age) {
    print age;
}
#"""

#使用 '#' 作为结束的符号

def isAlpha(char):
    if len(char) >1: return False;
    return "A" <= char <= "Z" or "a" <= char <= "z";

def isDigital(char):
    if len(char) >1: return False;
    return  "0" <= char <= "9";

class State(object):
    continueReceive = 0;
    identifier      = 1;
    string          = 2;
    operator        = 3;
    scope           = 4;
    number          = 5;
    error           = 6;

class TokenType(object):
    unknown        = -1;
    identifier     = State.identifier;
    string         = State.string;
    operator       = State.operator;
    scope          = State.scope;
    number         = State.number;
    descDictionary = {
        identifier: 'identifier',
        string: 'string',
        operator: 'operator',
        scope: 'scope',
        number:'number',
        -1: 'unknown',
        0:'continueReceive'
    }

    def __init__(self):
        self.value  = None;
        self.type   = TokenType.unknown;
        self.line   = -1;
        self.column = -1;


    def __str__(self):
        desc = TokenType.descDictionary[self.type];
        return '{\n  type:'+desc+ '\n  value:"'+self.value+'"'+'\n  line:'+str(self.line)+'\n  column:'+str(self.column)+"\n}\n";


class Scanner(object):
    keywords  = ['class', 'const', 'var', 'function', 'return', 'break', 'while', 'for', 'in'];
    operators = ['+', '-', '*', '/', '(', ')','[',']', '.', ',' ,'=','^','>','<','?','&','','|','@','%','!','_'];
    scopes    = ['{','}',';',':'];

    def __init__(self,text):
        self.state                  = State.continueReceive;
        self.tokens                 = [];
        self.buffer                 = [];
        self.charIndex              = 0;
        self.text                   = text;
        self.textLength             = len(text);
        self.stringStartSymbolCount = 0;
        self.line                   = 0;
        self.column                 = 0;

    def getNextChar(self):
        if 0 <= self.charIndex <= self.textLength - 1:
            char = self.text[self.charIndex];
            self.charIndex += 1;
            return char;
        return None;

    def scan(self):
        while True:
            char = self.getNextChar();
            if char == '#': break;

            # 记录之前的状态
            # record the previous state
            oldState = self.state;
            changed = self.setState(char);

            if changed:
                if len(self.buffer):
                    stringBlock = ''.join(self.buffer);
                    token = self.makeToken(stringBlock, oldState, self.line, self.column);
                    self.tokens.append(token);
                    # self.tokens.append(stringBlock);
                    self.buffer = [];

            if self.state == State.identifier:
                self.buffer.append(char);
            elif self.state == State.number:
                self.buffer.append(char);
            elif self.state == State.operator:
                self.buffer.append(char);
            elif self.state == State.scope:
                self.buffer.append(char);
            elif self.state == State.string:
                if char != '"' and char != "'": self.buffer.append(char);
            else:
                pass

            if char == '\n':
                self.line += 1;
                self.column = 0;
            else:
                self.column += 1;

        for i in self.tokens:
            print i;

    def makeToken(self,stringBlock,state,line,column):
        token = TokenType();
        token.type = state;
        token.value = stringBlock;
        token.line  = line;
        token.column = column;
        return token;

    #设置状态
    def setState(self,char):

        # 标记状态是否改变 用以清空buffer
        # mark when the state changed in order to clear the buffer
        stateChanged = False;
        if isAlpha(char):
            # 字符串输入状态
            if self.state == State.string:
                pass
            else:
                if self.state != State.identifier:
                    if char == 'e' and self.state == State.number:
                        pass
                    else:
                        stateChanged = True;
                        self.state = State.identifier

        elif isDigital(char):
            if self.state == State.identifier or self.state == State.string:
                # 标识之中输入数字状态不变
                pass
            elif self.state!= State.number:
                # 改变状态为 进入输入数字
                self.state = State.number;
                stateChanged = True;

        elif char == '"' or char =="'":
            self.stringStartSymbolCount += 1;
            if self.stringStartSymbolCount == 1:
                # 进入字符串输入
                self.state = State.string;

            elif self.stringStartSymbolCount == 2:
                # 结束字符串输入
                self.state = State.continueReceive;
                self.stringStartSymbolCount = 0;
            stateChanged = True;

        elif char == ' ' or char == '\n':
            if self.state != State.string:
                self.state = State.continueReceive;
                stateChanged = True;

        elif char in Scanner.operators:
            # 字符串输入模式
            if self.state == State.string:
                pass
            else:
                #特殊处理
                if char == '.':
                    # 小数识别状态
                    # enter the  float number state
                    if self.state == State.number:
                        pass

                    # 标识符状态 enter the identifier state
                    # elif self.state == State.identifier:
                    #     stateChanged = True;
                    #     self.state = State.operator;
                    # 当处于空状态（等待接受状态）或者操作符状态切换到数字状态
                    # switch to the number state when the next state is State.continueReceive or State.operator
                    elif self.state == State.continueReceive:
                        self.state = State.number
                        stateChanged = True;
                    else:
                        stateChanged = True;
                        self.state = State.operator;

                elif char == '_':
                    # 带下划线的标识符
                    # the identifier contains '_'
                    if self.state == State.identifier:
                        pass;
                    # 带下划线的标识符
                    # the identifier contains '_'
                    elif self.state == State.continueReceive or self.state == State.operator:
                        self.state = State.identifier;
                        stateChanged = True;
                    else:
                        self.state = State.operator;
                        stateChanged = True;
                # 直接切换状态
                # change the state to number immediately
                else:
                    self.state = State.operator;
                    stateChanged = True;

        elif char in Scanner.scopes:
            # 如果不是在字符串识别模式
            if self.state != State.string:
                self.state = State.scope;
                stateChanged = True;

        else:
            self.state = State.error;
            stateChanged = True;
            print("char can not be handled：" + char);

        return stateChanged;

Scanner = Scanner(codeTemp);
Scanner.scan();
