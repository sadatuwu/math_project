import sympy as smp
import re

class ExactDE:
    def __init__(self, equation):
        self.__eqn = equation  #private
        self.__M, self.__N= self.__extractMN() #private
        self.exact = self.__checkExactness(self.__M,self.__N); #public: rturns boolean value of exactness
        self.sol = None  #public : returns a string of solution
        if(self.exact) : self.sol = self.findSol()
        else: self.sol = "The equation is Not exact."


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
        return smp.sympify(_M), smp.sympify(_N)


    def __checkExactness(self, M , N):
        '''
        IN THIS STEP, dM/dy and dN/dx is calculated
        to check exactness
        '''
        x , y = smp.symbols("x y")
        dMdy = smp.diff(M,y)
        dNdx = smp.diff(N,x)
        exact = (dMdy == dNdx)
        return exact

    
    def findSol(self):
        x,y = smp.symbols("x y")
        M = self.__M ; N = self.__N

        F = smp.integrate(M,x)

        dFdy = smp.diff(F,y)

        dG = N - dFdy
        G = smp.integrate(dG, y)
        ans = F + G

        return self.decode(ans)+"= Constant";
        


    def encode(self, eqn):
        eqn = eqn.replace("xy", "x*y")
        eqn = re.sub(r'(\d+)([a-zA-Z(])', r'\1*\2', eqn)
        eqn = re.sub(r'([a-zA-Z)])(' + ')|('.join(['sin', 'cos', 'tan', 'exp']) + r')', r'\1*\2', eqn)

        return eqn

    def decode(self, eqn):
        eqn_str = str(eqn)

        eqn_str = re.sub(r'x\*\*([\d.]+)', r'x^{\1}', eqn_str)
        eqn_str = re.sub(r'y\*\*([\d.]+)', r'y^{\1}', eqn_str)
        eqn_str = re.sub(r'\*\*', r'^', eqn_str)
        
        return eqn_str.replace("*", "")



'''EXAMPLE USE:'''

eqn = input("Enter Differential Equation: ")
de = ExactDE(eqn)
print("Exact" if de.exact else "Not exact")  #example call of .exact
print("Solution: "+de.sol)  #example call of .sol


