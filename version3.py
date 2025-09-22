# crear usuarios/cursos, inscribir, crear evaluaciones y registrar calificaciones.

class Usuario:
    def __init__(self, id_usuario, nombre, correo):
        self.id = id_usuario
        self.nombre = nombre
        self.email = correo

class Estudiante(Usuario):
    def __init__(self, id_usuario, nombre, correo, carnet):
        super().__init__(id_usuario, nombre, correo)
        self.carnet = carnet
        self.cursos_inscritos = []

    def inscribir_curso(self, curso):
        if curso.codigo in [c.codigo for c in self.cursos_inscritos]:
            raise Exception("Estudiante ya inscrito")
        self.cursos_inscritos.append(curso)


class Instructor(Usuario):
    def __init__(self, id_usuario, nombre, correo, departamento):
        super().__init__(id_usuario, nombre, correo)
        self.departamento = departamento


class Evaluacion:
    def __init__(self, id_eval, titulo, max_puntos, tipo="gen"):
        self.id = id_eval
        self.titulo = titulo
        self.max_puntos = max_puntos
        self.tipo = tipo
        self.calificaciones = {}  

    def registrar_calificacion(self, id_estudiante, puntos):
        if puntos < 0 or puntos > self.max_puntos:
            raise ValueError("Puntos fuera de rango")
        self.calificaciones[id_estudiante] = puntos


class Curso:
    def __init__(self, nombre, codigo, instructor):
        self.nombre = nombre
        self.codigo = codigo
        self.instructor = instructor
        self.estudiantes = []
        self.evaluaciones = []

    def inscribir(self, estudiante):
        if estudiante.carnet in [e.carnet for e in self.estudiantes]:
            raise Exception("Estudiante ya inscrito")
        self.estudiantes.append(estudiante)
        estudiante.inscribir_curso(self)

    def agregar_evaluacion(self, evaluacion):
        self.evaluaciones.append(evaluacion)


class Plataforma:
    # Clase que gestiona colecciones de usuarios y cursos
    def __init__(self):
        self.usuarios = {}  
        self.cursos = {}  

    def registrar_usuario(self, usuario):
        if usuario.id in self.usuarios:
            raise Exception("Usuario ya registrado")
        self.usuarios[usuario.id] = usuario

    def crear_curso(self, nombre, codigo, instructor_id):
        if codigo in self.cursos:
            raise Exception("Código de curso ya existe")
        instructor = self.usuarios.get(instructor_id)
        if not instructor:
            raise Exception("Instructor no encontrado")
        curso = Curso(nombre, codigo, instructor)
        self.cursos[codigo] = curso
        return curso

    def inscribir_estudiante(self, codigo_curso, estudiante_id):
        curso = self.cursos.get(codigo_curso)
        estudiante = self.usuarios.get(estudiante_id)
        if not curso or not estudiante:
            raise Exception("Curso o estudiante no encontrado")
        curso.inscribir(estudiante)

    def promedio_estudiante_en_curso(self, codigo_curso, carnet_estudiante):
        curso = self.cursos.get(codigo_curso)
        if not curso:
            raise Exception("Curso no encontrado")
        # buscar id_estudiante por carnet
        id_est = None
        for u in self.usuarios.values():
            if hasattr(u, "carnet") and u.carnet == carnet_estudiante:
                id_est = u.id
        if id_est is None:
            raise Exception("Estudiante no encontrado")
        # calcular promedio: suma de calificaciones / número de evaluaciones
        suma = 0
        cuenta = 0
        for ev in curso.evaluaciones:
            if id_est in ev.calificaciones:
                suma += ev.calificaciones[id_est]
                cuenta += 1
        return suma / cuenta

