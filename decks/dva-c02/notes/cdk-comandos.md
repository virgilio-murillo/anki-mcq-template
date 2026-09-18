# AWS CDK: bootstrap, synth, context e import

## La pregunta

¿Qué hace cada comando del CDK CLI? Cada uno tiene una función distinta y es fácil confundirlos.

**Respuesta correcta (B):**

- **bootstrap**: provisiona los recursos base del entorno.
- **synth**: genera la plantilla CloudFormation.
- **context**: cachea datos del entorno (AZs, VPCs).
- **import**: trae recursos existentes al stack.

---

## Los 4 comandos de un vistazo

```mermaid
flowchart LR
    B(bootstrap<br/>prepara la cuenta+region) 
    S(synth<br/>codigo -> plantilla CFN)
    C(context<br/>cachea AZs, VPCs)
    I(import<br/>adopta recursos existentes)
    style B fill:#89b4fa,color:#1e1e2e
    style S fill:#a6e3a1,color:#1e1e2e
    style C fill:#f9e2af,color:#1e1e2e
    style I fill:#cba6f7,color:#1e1e2e
```

---

## `cdk bootstrap` — preparar el entorno

Se corre **una sola vez por cuenta + región**. Crea la infraestructura que CDK necesita para desplegar:

```mermaid
flowchart TB
    BOOT(cdk bootstrap) --> S3(Bucket S3<br/>para assets: Lambda, Docker)
    BOOT --> IAM(Roles IAM<br/>de despliegue)
    BOOT --> ECR(Repositorio ECR<br/>para imagenes de contenedor)
    style BOOT fill:#89b4fa,color:#1e1e2e
```

Sin bootstrap, un `deploy` que use assets falla porque no hay dónde subirlos.

---

## `cdk synth` — compilar a CloudFormation

Traduce tu código CDK (TypeScript, Python, Java...) a una **plantilla CloudFormation**:

```mermaid
flowchart LR
    CODE(Codigo CDK<br/>TypeScript / Python) -->|cdk synth| TPL(Plantilla CloudFormation<br/>JSON / YAML)
    style CODE fill:#a6e3a1,color:#1e1e2e
    style TPL fill:#f9e2af,color:#1e1e2e
```

Es como un "compilador": de código de alto nivel a la plantilla que CloudFormation sabe ejecutar. No despliega nada, solo genera el template.

---

## `cdk context` — cachear datos del entorno

Cuando CDK necesita datos reales de tu cuenta (qué AZs hay, qué VPCs existen), los consulta y los **guarda en `cdk.context.json`** para reutilizarlos:

```mermaid
flowchart LR
    Q(CDK pregunta:<br/>que AZs / VPCs hay) -->|consulta una vez| AWS(Cuenta AWS)
    AWS -->|guarda respuesta| CACHE(cdk.context.json)
    CACHE -->|reutiliza en synth| REP(Builds reproducibles)
    style CACHE fill:#f9e2af,color:#1e1e2e
    style REP fill:#a6e3a1,color:#1e1e2e
```

Beneficio: las builds son **reproducibles**. El resultado no cambia entre corridas aunque el entorno cambie. `cdk context` te deja ver y limpiar ese caché.

---

## `cdk import` — adoptar recursos existentes

Incorpora a un stack recursos que **ya existen** (creados a mano o por otra herramienta), usando los *resource imports* de CloudFormation:

```mermaid
flowchart LR
    EX(Recurso existente<br/>creado fuera de CDK) -->|cdk import| STK(Stack CDK<br/>ahora lo gestiona)
    style EX fill:#f38ba8,color:#1e1e2e
    style STK fill:#cba6f7,color:#1e1e2e
```

CDK empieza a gestionar el recurso **sin recrearlo ni borrarlo**. Útil para migrar infra existente a CDK.

---

## Tabla comparativa

| Comando | Qué hace | Cuándo se usa |
|---|---|---|
| **bootstrap** | Provisiona bucket S3, roles IAM y ECR en la cuenta+región | Una vez por entorno |
| **synth** | Compila el código CDK a plantilla CloudFormation | Cada vez que cambias el código |
| **context** | Cachea AZs, VPCs y otros datos del entorno | Automático al sintetizar; lo gestionas para reproducibilidad |
| **import** | Adopta recursos ya existentes en un stack | Al migrar infra existente a CDK |

---

## Por qué fallan las otras opciones

Todas **intercambian las definiciones**:

| Opción | Error |
|---|---|
| A | Dice que bootstrap importa recursos y synth cachea; falso |
| C | Dice que synth importa y context genera el template; falso |
| D | Dice que synth provisiona el entorno e import cachea datos; falso |

Solo **B** asigna las cuatro funciones correctamente.

---

## El flujo típico de trabajo

```mermaid
flowchart LR
    A(cdk bootstrap<br/>una vez por entorno) --> B(escribir codigo CDK)
    B --> C(cdk synth<br/>genera plantilla)
    C --> D(cdk deploy<br/>crea/actualiza stack)
    style A fill:#89b4fa,color:#1e1e2e
    style C fill:#a6e3a1,color:#1e1e2e
    style D fill:#cba6f7,color:#1e1e2e
```

---

## Resumen de examen (DVA-C02)

- **bootstrap** = prepara la cuenta+región (S3 assets, IAM, ECR). Una vez por entorno.
- **synth** = código → plantilla CloudFormation. No despliega.
- **context** = caché de datos del entorno (AZs, VPCs) en `cdk.context.json` → builds reproducibles.
- **import** = adopta recursos existentes en un stack sin recrearlos.
- Flujo: **bootstrap → escribir código → synth → deploy**.
