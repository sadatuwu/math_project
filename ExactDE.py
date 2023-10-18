from sympy import *
import re

class ExactDE:
    def __init__(self, equation):
        self.__eqn = equation  #private
        self.__M, self.__N= self.__extractMN() #private
        self.__dMdy, self.__dNdx = self.__checkExactness(self.__M,self.__N); 
        self.exact = (self.__dMdy == self.__dNdx)#public: rturns boolean value of exactness
        self.sol = None  #public : returns a string of solution
        if(self.exact) : self.sol = self.findSol()
        else: self.sol = "The equation is Not exact."


    def getInfo(self):
        # return self.__eqn
        print("Equation is:",self.__eqn);
        print("dM/dy=", self.__dMdy)
        print("dN/dx=", self.__dNdx)
        print("Exact? =", self.exact)


    def __extractMN(self):
        i =0;
        s= self.__eqn
        n = len(s)
        M = ""
        while(i<n):
            if s[i]+s[i+1] == "dx" : break
            M += s[i]
            i+=1
        i+=2
        N=""
        while(i<n):
            if s[i]+s[i+1] =='dy' : break
            N += s[i]
            i+=1

        
        _M = self.encode(M)
        _N = self.encode(N)
        return sympify(_M), sympify(_N)


    def __checkExactness(self, M , N):
        '''
        IN THIS STEP, dM/dy and dN/dx is calculated
        to check exactness
        '''
        x , y = symbols("x y")
        dMdy = diff(M,y)
        dNdx = diff(N,x)
        exact = (dMdy == dNdx)
        return dMdy, dNdx;

    
    def findSol(self):
        x,y = symbols("x y")
        M = self.__M ; N = self.__N

        F = integrate(M,x, conds='separate')

        dFdy = diff(F,y)

        dG = N - dFdy
        G = integrate(dG, y, conds='separate')

        ans = F + G
    

        return self.decode(ans)+"= Constant";



    def encode(self, eqn):
        eqn = eqn.replace("xy", "x*y")
        eqn = eqn.replace("yx", "y*x")
        eqn = re.sub(r'(\d+)([a-zA-Z(])', r'\1*\2', eqn)

        # Handle functions explicitly
        all_functions = ['sin', 'cos', 'tan', 'exp', 'sec', 'csc', 'cot', 'asin', 'acos', 'atan', 'asec', 'acsc', 'acot']
        for func in all_functions:
            eqn = eqn.replace(f"{func}(x)", f"{func}(x)")

        # Correct handling for tan(y) and 1+y^2
        eqn = re.sub(r'tan\(([^)]+)\)', r'tan(\1)', eqn)
        eqn = re.sub(r'1\+y\*\*2', r'1+y**2', eqn)

        eqn = re.sub(r'([a-zA-Z)])(' + '|'.join(all_functions) + r')\(', r'\1(\2)', eqn)

        return eqn



    def decode(self, eqn):
        eqn_str = str(eqn)

        eqn_str = re.sub(r'x\*\*([\d.]+)', r'x^{\1}', eqn_str)
        eqn_str = re.sub(r'\*\*', r'^', eqn_str)
        
        return eqn_str.replace("*", "")



'''EXAMPLE USE:'''

eqn = input("Enter Differential Equation: ")
de = ExactDE(eqn)
print("Solution: "+de.sol)


