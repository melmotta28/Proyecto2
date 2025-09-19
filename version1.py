class Usuario:
    def __init__(self, id_usuario, nombre, correo):
        self.id = id_usuario
        self.nombre = nombre
        self.email = correo

    def __str__(self):
        return f"{self.nombre} ({self.email})"


class Estudiante(Usuario):
    def __init__(self, id_usuario, nombre, correo, carnet):
        super().__init__(id_usuario, nombre, correo)
        self.carnet = carnet
        self.cursos_inscritos = []


class Instructor(Usuario):
    def __init__(self, id_usuario, nombre, correo, departamento):
        super().__init__(id_usuario, nombre, correo)
        self.depto = departamento


class Curso:
    def __init__(self, nombre, codigo, instructor):
        self.nombre = nombre
        self.codigo = codigo
        self.instructor = instructor
        self.estudiantes = []  
        self.evaluaciones = []  

    def inscribir(self, estudiante):
        self.estudiantes.append(estudiante)

    def listar_estudiantes(self):
        return [e.nombre for e in self.estudiantes]


