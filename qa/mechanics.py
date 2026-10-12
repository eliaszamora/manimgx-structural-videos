"""Referencia independiente para auditar el voladizo de Euler-Bernoulli.

Convenciones: x de empotramiento a punta, v arriba positivo;
M positivo asociado a concavidad positiva, V=dM/dx.
Diagrama: M positivo bajo eje, M negativo sobre eje.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Cantilever:
    length: float = 6.0
    force: float = 10.0       # magnitud P descendente
    EI: float = 12000.0      # constante positiva, para referencia normalizada

    def deflection(self,x:float)->float:
        return -(self.force*x*x*(3*self.length-x))/(6*self.EI)

    def slope(self,x:float)->float:
        return -(self.force*x*(2*self.length-x))/(2*self.EI)

    def curvature(self,x:float)->float:
        return -(self.force*(self.length-x))/self.EI

    def moment(self,x:float)->float:
        return -self.force*(self.length-x)

    def shear(self,x:float)->float:
        return self.force

    def normalized_deflection(self,u:float)->float:
        return -(u*u*(3-u))/2.0
