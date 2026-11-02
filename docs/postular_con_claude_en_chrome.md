# Postular con Claude en Chrome

Instrucciones para pegarle a **Claude en Chrome** (la extensión del navegador) para que se postule por Juan a ofertas remotas de empresas de afuera.

## Antes de empezar

1. Instalá la extensión **Claude in Chrome** y abrí Chrome con tu sesión de LinkedIn iniciada.
2. Tené a mano el **Radar Laboral** (`https://claude.ai/artifact/QqYmQcmQcNSyjDrHHU3yYd`) y una carpeta en tu compu con:
   - `CV Juan Faure Santamarina - EN.pdf` (CV general en inglés)
   - `CV Juan Faure Santamarina - ES.pdf` (CV general en español)
   - Los CVs y cartas por empresa que bajes del Radar.
3. Hacé la primera tanda con pocas ofertas (5 a 10) y revisá cada formulario antes de que lo envíe.

## Prompt para pegar en Claude en Chrome

```
Sos mi asistente de búsqueda laboral. Quiero que me postules a trabajos REMOTOS de empresas de afuera (EE.UU., Europa u otras) que contraten desde Argentina o Latinoamérica.

MI PERFIL
- Juan Faure Santamarina, Buenos Aires, Argentina (UTC-3). Inglés C2, español nativo.
- Email: juanfauresantamarina@gmail.com · Tel: +54 911 5871-4730
- Experiencia: Administración (cobranzas, pagos, conciliaciones, costos) en PROTA (jun 2026–hoy); Jefe de Operaciones en Lauken, agencia B2B (feb 2025–sep 2026); Fundador de Moturi (mar 2024–hoy); Analista Comercial en Cavalier Polo (jul 2023–sep 2024).
- Herramientas: Excel, SQL, N8N, Clay, Apify, Supabase, IA generativa (Claude, ChatGPT).
- Estudios: Administración de Empresas (Universidad Siglo 21, en curso); Lic. en Actividad Física y Deportiva (USAL, 2024); Diplomatura en Coaching Organizacional y Liderazgo (USAL, 2022).
- NO usé QuickBooks, Shopify, Salesforce, HubSpot ni SAP en profundidad: nunca digas que sí.

QUÉ BUSCAR
- En LinkedIn Empleos: ubicación "Latin America" o "Argentina", filtro "Remoto", "Solicitud sencilla" (Easy Apply), publicadas en la última semana.
- Puestos: Operations Analyst, Operations Associate, Business Operations, Operations Coordinator, Process Analyst, Executive Assistant, Administrative Assistant, Virtual Assistant, Accounts Payable, Bookkeeper, Finance Operations, Procurement Analyst, Project Coordinator, Automation Specialist.
- También podés usar las ofertas del Radar Laboral marcadas "Para postular" en el filtro "Afuera".

QUÉ DESCARTAR
- Ofertas que exigen vivir en otro país (ej.: "must be based in Mexico/Brazil/US").
- Presenciales o híbridas fuera de Buenos Aires.
- Puestos senior/manager/director que piden 5+ años.
- Puestos que piden experiencia obligatoria en herramientas que no uso.

CÓMO POSTULAR
1. Usá el CV en inglés salvo que la oferta esté en español. Si la oferta está en el Radar con CV propio, usá ese.
2. Respondé cada pregunta del formulario SOLO con información de mi perfil. Si una pregunta pide algo que no sé (salario pretendido, años en una herramienta que no usé, un caso concreto), FRENÁ y preguntame.
3. Horario: puedo trabajar en horario de EE.UU. Si piden un rango en Pacific Time, preguntame antes de responder.
4. Antes de tocar "Enviar", mostrame el formulario completo y esperá mi OK.
5. Máximo 10 postulaciones por sesión, con pausas entre cada una.
6. Al terminar, pasame una lista: empresa, puesto, link y si quedó enviada.
```

## Después de cada tanda

- Marcá las enviadas como **Postulado** en el Radar Laboral.
- Si querés, pasale a Claude Code la lista que te dio Claude en Chrome y las cargo yo en el tracker.

## Riesgos a tener en cuenta

- **LinkedIn no permite la automatización.** Si detecta mucha actividad automática puede restringir o suspender tu cuenta. Por eso el límite de 10 por sesión y la confirmación antes de enviar.
- **CAPTCHA y verificaciones:** esos pasos los tenés que hacer vos.
- **Una postulación enviada no se puede deshacer.**
