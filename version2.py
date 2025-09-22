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
        # lista de cursos inscritos
        self.cursos_inscritos = []

    def inscribir_curso(self, curso):
        #agrega curso a la lista del estudiante (evita los dupplicados)
        if curso.codigo not in [c.codigo for c in self.cursos_inscritos]:
            self.cursos_inscritos.append(curso)
        else:
            raise Exception("Estudiante ya inscrito en el curso")


class Instructor(Usuario):
    def __init__(self, id_usuario, nombre, correo, departamento):
        super().__init__(id_usuario, nombre, correo)
        self.departamento = departamento


class Evaluacion:
    # Evaluacion base, faltan subclases
    def __init__(self, titulo, max_puntos):
        self.titulo = titulo
        self.max_puntos = max_puntos
        #registro de calificaciones por id de estudiante
        self.calificaciones = {}

    def registrar_calificacion(self, id_estudiante, puntos):
        # Guarda la calificacion (aun falta que valide el rango)
        self.calificaciones[id_estudiante] = puntos


class Curso:
    def __init__(self, nombre, codigo, instructor):
        self.nombre = nombre
        self.codigo = codigo
        self.instructor = instructor
        self.estudiantes = []
        self.evaluaciones = []

    def inscribir(self, estudiante):
        #evita duplicados comprobando el carnet
        if estudiante.carnet in [e.carnet for e in self.estudiantes]:
            raise Exception("Estudiante ya inscrito en el curso")
        self.estudiantes.append(estudiante)  
        estudiante.inscribir_curso(self)

    def agregar_evaluacion(self, evaluacion):
        self.evaluaciones.append(evaluacion)

#aun faltan Plataforma gestion global, los metodos de consulta y los reportes.
