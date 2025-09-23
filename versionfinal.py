from typing import Dict, List, Optional

class Usuario:
    def __init__(self, id_usuario: str, nombre: str, correo: str):
        self.id = id_usuario
        self.nombre = nombre
        self.email = correo

    def __str__(self):
        return f"{self.nombre} ({self.email})"

class Estudiante(Usuario):
    def __init__(self, id_usuario: str, nombre: str, correo: str, carnet: str):
        super().__init__(id_usuario, nombre, correo)
        self.carnet = carnet
        self.cursos_inscritos: List['Curso'] = []

    def inscribir_curso(self, curso: 'Curso'):
        if any(c.codigo == curso.codigo for c in self.cursos_inscritos):
            raise ValueError("Estudiante ya inscrito en ese curso")
        self.cursos_inscritos.append(curso)

class Profesor(Usuario):
    def __init__(self, id_usuario: str, nombre: str, correo: str, departamento: str):
        super().__init__(id_usuario, nombre, correo)
        self.departamento = departamento

class Evaluacion:
    def __init__(self, id_eval: int, titulo: str, max_puntos: float, peso: float = 1.0, **kwargs):
        self.id = id_eval
        self.titulo = titulo
        self.max_puntos = float(max_puntos)
        if self.max_puntos <= 0:
            raise ValueError("max_puntos debe ser > 0")
        self.peso = float(peso)
        self.calificaciones: Dict[str, float] = {}

    def registrar_calificacion(self, id_estudiante: str, puntos: float):
        puntos = float(puntos)
        if puntos < 0 or puntos > self.max_puntos:
            raise ValueError("Puntos fuera de rango")
        self.calificaciones[id_estudiante] = puntos

    def obtener_porcentaje(self, id_estudiante: str) -> Optional[float]:
        if id_estudiante not in self.calificaciones:
            return None
        return (self.calificaciones[id_estudiante] / self.max_puntos) * 100.0

class Examen(Evaluacion):
    def __init__(self, id_eval: int, titulo: str, max_puntos: float, peso: float = 1.0, **kwargs):
        super().__init__(id_eval, titulo, max_puntos, peso=peso, **kwargs)
        self.tipo = "examen"

class Tarea(Evaluacion):
    def __init__(self, id_eval: int, titulo: str, max_puntos: float, peso: float = 1.0, **kwargs):
        super().__init__(id_eval, titulo, max_puntos, peso=peso, **kwargs)
        self.tipo = "tarea"

class Curso:
    def __init__(self, nombre: str, codigo: str, profesor: Profesor):
        self.nombre = nombre
        self.codigo = codigo
        self.profesor = profesor
        self.estudiantes: List[Estudiante] = []
        self.evaluaciones: List[Evaluacion] = []

    def inscribir(self, estudiante: Estudiante):
        if any(e.carnet == estudiante.carnet for e in self.estudiantes):
            raise ValueError("Estudiante ya inscrito en el curso")
        self.estudiantes.append(estudiante)
        estudiante.inscribir_curso(self)

    def agregar_evaluacion(self, evaluacion: Evaluacion):
        if any(ev.id == evaluacion.id for ev in self.evaluaciones):
            raise ValueError("Evaluación con ID duplicado en este curso")
        self.evaluaciones.append(evaluacion)

    def obtener_promedio_estudiante(self, id_estudiante: str) -> Optional[float]:
        suma_ponderada = 0.0
        suma_pesos = 0.0
        for ev in self.evaluaciones:
            pct = ev.obtener_porcentaje(id_estudiante)
            if pct is not None:
                suma_ponderada += pct * ev.peso
                suma_pesos += ev.peso
        if suma_pesos == 0:
            return None
        return suma_ponderada / suma_pesos

    def listar_estudiantes(self) -> List[str]:
        return [e.nombre for e in self.estudiantes]

class Plataforma:
    def __init__(self):
        self.usuarios: Dict[str, Usuario] = {}
        self.cursos: Dict[str, Curso] = {}
        self.next_eval_id = 1

    def registrar_usuario(self, usuario: Usuario):
        if usuario.id in self.usuarios:
            raise ValueError("Usuario ya registrado")
        self.usuarios[usuario.id] = usuario

    def crear_curso(self, nombre: str, codigo: str, profesor_id: str) -> Curso:
        if codigo in self.cursos:
            raise ValueError("Código de curso ya existente")
        profesor = self.usuarios.get(profesor_id)
        if not isinstance(profesor, Profesor):
            raise ValueError("Profesor inválido o no encontrado")
        curso = Curso(nombre, codigo, profesor)
        self.cursos[codigo] = curso
        return curso

    def inscribir_estudiante(self, codigo_curso: str, estudiante_id: str):
        curso = self.cursos.get(codigo_curso)
        estudiante = self.usuarios.get(estudiante_id)
        if curso is None:
            raise ValueError("Curso no encontrado")
        if not isinstance(estudiante, Estudiante):
            raise ValueError("Usuario no es estudiante o no encontrado")
        curso.inscribir(estudiante)

    def crear_evaluacion(self, codigo_curso: str, tipo: str, titulo: str, max_puntos: float, peso: float = 1.0, **kwargs) -> Evaluacion:
        curso = self.cursos.get(codigo_curso)
        if curso is None:
            raise ValueError("Curso no encontrado")
        id_eval = self.next_eval_id
        self.next_eval_id += 1
        if tipo.lower() == "examen":
            ev = Examen(id_eval, titulo, max_puntos, peso=peso, **kwargs)
        elif tipo.lower() == "tarea":
            ev = Tarea(id_eval, titulo, max_puntos, peso=peso, **kwargs)
        else:
            ev = Evaluacion(id_eval, titulo, max_puntos, peso=peso, **kwargs)
        curso.agregar_evaluacion(ev)
        return ev

    def registrar_calificacion(self, codigo_curso: str, id_eval: int, estudiante_id: str, puntos: float):
        curso = self.cursos.get(codigo_curso)
        if curso is None:
            raise ValueError("Curso no encontrado")
        ev = next((e for e in curso.evaluaciones if e.id == id_eval), None)
        if ev is None:
            raise ValueError("Evaluación no encontrada en el curso")
        if not isinstance(self.usuarios.get(estudiante_id), Estudiante):
            raise ValueError("Usuario no es estudiante o no existe")
        ev.registrar_calificacion(estudiante_id, puntos)

    def obtener_promedio_estudiante_en_curso(self, codigo_curso: str, estudiante_id: str) -> Optional[float]:
        curso = self.cursos.get(codigo_curso)
        if curso is None:
            raise ValueError("Curso no encontrado")
        return curso.obtener_promedio_estudiante(estudiante_id)

    def reporte_estudiantes_promedio_bajo(self, codigo_curso: str, umbral_porcentaje: float) -> List[Dict]:
        curso = self.cursos.get(codigo_curso)
        if curso is None:
            raise ValueError("Curso no encontrado")
        resultado = []
        for est in curso.estudiantes:
            prom = curso.obtener_promedio_estudiante(est.id)
            if prom is None:
                continue
            if prom < umbral_porcentaje:
                resultado.append({'id': est.id, 'nombre': est.nombre, 'promedio': round(prom, 2)})
        return resultado

    def listar_profesores(self) -> List[Profesor]:
        return [u for u in self.usuarios.values() if isinstance(u, Profesor)]

    def listar_cursos(self) -> List[Curso]:
        return list(self.cursos.values())

if __name__ == "__main__":
    pl = Plataforma()
    while True:
        print("\nMenú")
        print("1. Registrar profesor")
        print("2. Registrar estudiante")
        print("3. Crear curso")
        print("4. Inscribir estudiante en curso")
        print("5. Crear evaluación")
        print("6. Registrar calificación")
        print("7. Ver promedio de estudiante")
        print("8. Reporte de promedios bajos")
        print("9. Salir")
        print("10. Ver profesores registrados")
        print("11. Ver cursos registrados")
        op = input("Elige una opción: ")

        try:
            if op == "1":
                idu = input("ID profesor: ")
                nom = input("Nombre: ")
                cor = input("Correo: ")
                dep = input("Departamento: ")
                pl.registrar_usuario(Profesor(idu, nom, cor, dep))
                print("Profesor registrado.")
            elif op == "2":
                idu = input("ID estudiante: ")
                nom = input("Nombre: ")
                cor = input("Correo: ")
                car = input("Carnet: ")
                pl.registrar_usuario(Estudiante(idu, nom, cor, car))
                print("Estudiante registrado.")
            elif op == "3":
                nom = input("Nombre curso: ")
                cod = input("Código curso: ")
                prof = input("ID profesor: ")
                pl.crear_curso(nom, cod, prof)
                print("Curso creado.")
            elif op == "4":
                cod = input("Código curso: ")
                est = input("ID estudiante: ")
                pl.inscribir_estudiante(cod, est)
                print("Estudiante inscrito.")
            elif op == "5":
                cod = input("Código curso: ")
                tipo = input("Tipo (examen/tarea): ")
                tit = input("Título: ")
                maxp = float(input("Puntos máximos: "))
                peso = float(input("Peso: "))
                ev = pl.crear_evaluacion(cod, tipo, tit, maxp, peso=peso)
                print(f"Evaluación creada con ID {ev.id}")
            elif op == "6":
                cod = input("Código curso: ")
                ide = int(input("ID evaluación: "))
                est = input("ID estudiante: ")
                pts = float(input("Puntos obtenidos: "))
                pl.registrar_calificacion(cod, ide, est, pts)
                print("Calificación registrada.")
            elif op == "7":
                cod = input("Código curso: ")
                est = input("ID estudiante: ")
                prom = pl.obtener_promedio_estudiante_en_curso(cod, est)
                if prom is None:
                    print("Sin calificaciones registradas.")
                else:
                    print(f"Promedio: {round(prom,2)}%")
            elif op == "8":
                cod = input("Código curso: ")
                umb = float(input("Umbral (%): "))
                rep = pl.reporte_estudiantes_promedio_bajo(cod, umb)
                if not rep:
                    print("Ningún estudiante debajo del umbral.")
                else:
                    for r in rep:
                        print(r)
            elif op == "9":
                break
            elif op == "10":
                profs = pl.listar_profesores()
                if not profs:
                    print("No hay profesores registrados.")
                else:
                    for p in profs:
                        print(f"ID: {p.id}, Nombre: {p.nombre}, Correo: {p.email}, Dep: {p.departamento}")
            elif op == "11":
                cursos = pl.listar_cursos()
                if not cursos:
                    print("No hay cursos registrados.")
                else:
                    for c in cursos:
                        print(f"Código: {c.codigo}, Nombre: {c.nombre}, Profesor: {c.profesor.nombre}")
            else:
                print("Opción inválida.")
        except Exception as e:
            print("Error:", e)


