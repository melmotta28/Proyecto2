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
            raise Exception("Ya inscrito")
        self.cursos_inscritos.append(curso)


class Instructor(Usuario):
    def __init__(self, id_usuario, nombre, correo, departamento):
        super().__init__(id_usuario, nombre, correo)
        self.departamento = departamento


class Evaluacion:
    def __init__(self, id_eval, titulo, max_puntos, peso=1.0, tipo="gen"):
        self.id = id_eval
        self.titulo = titulo
        self.max_puntos = max_puntos
        self.peso = peso  #error con los pesos
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

    def obtener_promedio_estudiante(self, id_est):
        suma_ponderada = 0
        suma_pesos = 0
        for ev in self.evaluaciones:
            if id_est in ev.calificaciones:
                puntos = ev.calificaciones[id_est]
                suma_ponderada += puntos * ev.peso  # falta la normalizacion por max_puntos
                suma_pesos += ev.peso
        if suma_pesos == 0:
            return None
        #devuelve puntuacion absoluta en lugar de porcentaje
        return suma_ponderada / suma_pesos


class Plataforma:
    def __init__(self):
        self.usuarios = {}  # id - usuario
        self.cursos = {}    # codigo - curso
        self.next_eval_id = 1

    def registrar_usuario(self, usuario):
        if usuario.id in self.usuarios:
            raise Exception("Usuario duplicado")
        self.usuarios[usuario.id] = usuario

    def crear_curso(self, nombre, codigo, instructor_id):
        if codigo in self.cursos:
            raise Exception("Curso duplicado")
        instructor = self.usuarios.get(instructor_id)
        if not instructor or not isinstance(instructor, Instructor):
            raise Exception("Instructor invalido")
        curso = Curso(nombre, codigo, instructor)
        self.cursos[codigo] = curso
        return curso

    def inscribir_estudiante(self, codigo_curso, estudiante_id):
        curso = self.cursos.get(codigo_curso)
        estudiante = self.usuarios.get(estudiante_id)
        if not curso or not estudiante:
            raise Exception("Curso o estudiante no encontrado")
        curso.inscribir(estudiante)

    def crear_evaluacion(self, codigo_curso, titulo, max_puntos, peso=1.0, tipo="gen"):
        curso = self.cursos.get(codigo_curso)
        if not curso:
            raise Exception("Curso no encontrado")
        ev = Evaluacion(self.next_eval_id, titulo, max_puntos, peso=peso, tipo=tipo)
        self.next_eval_id += 1
        curso.agregar_evaluacion(ev)
        return ev

    def registrar_calificacion(self, codigo_curso, eval_id, estudiante_id, puntos):
        curso = self.cursos.get(codigo_curso)
        if not curso:
            raise Exception("Curso no encontrado")
        ev = None
        for e in curso.evaluaciones:
            if e.id == eval_id:
                ev = e
        if ev is None:
            raise Exception("Evaluacion no encontrada")
        ev.registrar_calificacion(estudiante_id, puntos)

    def reporte_estudiantes_promedio_bajo(self, codigo_curso, umbral):
        curso = self.cursos.get(codigo_curso)
        if not curso:
            raise Exception("Curso no encontrado")
        resultados = []
        for est in curso.estudiantes:
            prom = curso.obtener_promedio_estudiante(est.id)
            if prom is None:
                prom = 0
            if prom < umbral:
                resultados.append((est.nombre, prom))
        return resultados

