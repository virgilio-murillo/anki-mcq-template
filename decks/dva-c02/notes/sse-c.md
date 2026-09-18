# SSE-C explicado: "el cliente la provee en cada request"

## La idea en una frase

**SSE-C** = *Server-Side Encryption with Customer-provided keys* (cifrado del lado del servidor con claves provistas por el cliente).

S3 cifra y descifra tus objetos por ti (por eso es *server-side*), pero **la clave de cifrado es tuya y AWS nunca la guarda**. Como AWS no la almacena, **tú tienes que enviar la clave en cada petición** (`PUT` para subir, `GET` para bajar). De ahí la frase: *"el cliente la provee en cada request"*.

---

## La analogía del casillero

Imagina un casillero con un guardia:

- El **guardia** (S3) es quien físicamente cierra y abre la puerta (cifra/descifra).
- La **llave** (tu clave) es solo tuya. El guardia nunca se queda con una copia.
- Cada vez que quieres guardar o sacar algo, **traes tu llave**, el guardia la usa, y luego **la devuelve/olvida**.

Si pierdes la llave, ni el guardia ni nadie puede abrir el casillero. Tus datos quedan cifrados para siempre.

```mermaid
flowchart LR
    A(Tu llave<br/>solo tuya) -->|la traes cada vez| B(Guardia S3<br/>cifra y descifra)
    B -->|olvida la llave<br/>al terminar| C(Casillero<br/>objeto cifrado)
    style A fill:#89b4fa,color:#1e1e2e
    style B fill:#a6e3a1,color:#1e1e2e
    style C fill:#f9e2af,color:#1e1e2e
```

---

## Flujo de una SUBIDA (PUT) con SSE-C

```mermaid
sequenceDiagram
    participant Cliente
    participant S3
    Cliente->>S3: PUT objeto + clave (en headers HTTP)
    Note over S3: S3 cifra el objeto<br/>usando tu clave
    Note over S3: S3 guarda el objeto CIFRADO<br/>y descarta la clave
    S3-->>Cliente: 200 OK (guarda un HMAC de la clave<br/>para validar despues)
    Note over S3: AWS NO almacena tu clave
```

## Flujo de una DESCARGA (GET) con SSE-C

```mermaid
sequenceDiagram
    participant Cliente
    participant S3
    Cliente->>S3: GET objeto + la MISMA clave (en headers HTTP)
    Note over S3: S3 valida que la clave coincida<br/>(comparando el HMAC guardado)
    Note over S3: S3 descifra el objeto<br/>con tu clave
    S3-->>Cliente: 200 OK + objeto descifrado
    Note over S3: S3 descarta la clave de nuevo
```

Punto clave: si en el `GET` mandas una clave distinta (o no la mandas), **S3 rechaza la petición**. No puede descifrar sin la clave correcta.

---

## Requisitos técnicos de SSE-C

- **HTTPS es obligatorio.** Como la clave viaja en cada request, S3 rechaza SSE-C sobre HTTP (viajaría en texto plano). Debes usar HTTPS siempre.
- La clave se manda en headers específicos:
  - `x-amz-server-side-encryption-customer-algorithm: AES256`
  - `x-amz-server-side-encryption-customer-key: <tu clave en base64>`
  - `x-amz-server-side-encryption-customer-key-MD5: <MD5 de la clave>`
- Aplica a **cada** operación: `PUT`, `GET`, `HEAD`, `POST`, y también al `UploadPart` de multipart.

---

## Comparación: las tres formas de cifrado del lado del servidor

```mermaid
flowchart TB
    subgraph SSE-S3
        S1(AWS crea y gestiona la clave)
        S2(Tu no ves ni manejas nada)
        S3a(Header: AES256)
    end
    subgraph SSE-KMS
        K1(Clave en AWS KMS)
        K2(Permisos y auditoria via CloudTrail)
        K3(Header: aws:kms)
    end
    subgraph SSE-C
        C1(TU provees la clave)
        C2(AWS nunca la guarda)
        C3(La mandas en cada request via HTTPS)
    end
    style SSE-C fill:#f9e2af,color:#1e1e2e
```

| Aspecto | SSE-S3 | SSE-KMS | **SSE-C** |
|---|---|---|---|
| ¿Quién crea la clave? | AWS | AWS KMS (o la tuya en KMS) | **Tú** |
| ¿Dónde vive la clave? | En AWS | En AWS KMS | **Solo contigo** |
| ¿La envías en cada request? | No | No | **Sí, siempre** |
| ¿AWS puede descifrar sin ti? | Sí | Sí (con permisos KMS) | **No** |
| ¿HTTPS obligatorio? | No | No | **Sí** |
| Auditoría de uso de clave | Limitada | Sí (CloudTrail) | Tú la gestionas |
| Si pierdes la clave... | N/A | N/A | **Datos irrecuperables** |

---

## ¿Cuándo se usa SSE-C?

- Cuando por política o cumplimiento **no puedes dejar que AWS tenga tus claves**.
- Cuando ya tienes tu propio sistema de gestión de claves (KMS externo, HSM propio) y quieres control total.
- El costo: tú asumes toda la responsabilidad. Si pierdes la clave, **pierdes el acceso a los datos para siempre**. AWS no puede ayudarte a recuperarlos.

---

## Resumen de examen (DVA-C02)

- **SSE-C**: tú traes la clave; AWS cifra/descifra pero **no la guarda**.
- **"El cliente la provee en cada request"** = mandas la clave en los headers de **cada** `PUT` y `GET`.
- **HTTPS obligatorio** (la clave viaja en la petición).
- AWS guarda solo un **HMAC/hash** de la clave para validar, nunca la clave en sí.
- Pierdes la clave = pierdes los datos.
- Si el examen dice "el cliente gestiona las claves pero quiere que S3 haga el cifrado" → **SSE-C**.
- Si dice "el cliente cifra ANTES de subir" → eso ya es **client-side encryption**, no SSE-C.
