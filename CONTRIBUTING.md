# Contribuyendo al F1-Tutor-Bot

¡Gracias por tu interés en mejorar este proyecto! Como desarrollador, valoro mucho la calidad del código, la arquitectura y la colaboración abierta. Este documento describe cómo puedes participar de manera efectiva.

## ¿Cómo puedes ayudar?

- **Reportar errores:** Si encuentras un bug o un comportamiento inesperado, por favor abre un 'Issue' en este repositorio. Incluye detalles como:
    - Pasos para reproducir el error.
    - El entorno en el que lo ejecutaste.
    - Capturas de pantalla o logs (asegúrate de anonimizar tokens/credenciales).
- **Proponer mejoras:** Si tienes una idea para una nueva funcionalidad (ej. nuevas integraciones, optimización de RAG), abre un 'Issue' para discutirla antes de empezar a programar.
- **Pull Requests:** 1. Haz un fork del repositorio.
    2. Crea una rama nueva para tu característica (`git checkout -b feature/nombre-funcionalidad`).
    3. Realiza tus cambios, asegurando que sigan los principios de **Arquitectura Limpia**.
    4. Sube tu rama y crea un Pull Request detallando qué cambios realizaste y por qué.

## Estándar de Código
Este proyecto sigue una arquitectura limpia. Al contribuir, por favor asegúrate de:

- **Desacoplamiento:** Mantén la lógica de negocio (Use Cases) independiente de la infraestructura (APIs, DBs).
- **Seguridad:** NUNCA subas tokens, credenciales o claves de API al repositorio. Utiliza variables de entorno.
- **Calidad:** Escribe código claro y, si es posible, añade pruebas unitarias para nuevas funcionalidades.
- **Logs:** Asegúrate de seguir el patrón de filtrado de tokens en los logs para mantener la seguridad.

---
¡Tu ayuda hace que este bot sea mejor para todos los fanáticos de la Fórmula 1!
