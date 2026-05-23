---
name: tgs-validator
description: "Valida la coherencia interna de un analisis TGS: verifica que los nodos del diagrama existan como subsistemas y que las relaciones sean consistentes."
required_bins: [jq]
required_env: []
install: |
  echo "tgs-validator listo"
---

# Implementation

Recibir el analisis TGS en formato JSON como arg {analysis}.

Verificar las siguientes reglas de coherencia:

1. Cada nodo mencionado en diagrama_mermaid debe aparecer como elemento o subsistema en el analisis.
2. Cada relacion en la lista de relaciones debe referenciar elementos que existan en elementos o subsistemas.
3. El tipo de sistema debe ser coherente con la presencia o ausencia de retroalimentacion.
4. El nivel de complejidad debe ser coherente con la cantidad de subsistemas y relaciones.

Usar jq para parsear el JSON del analisis e inspeccionar los campos:
subsistemas[].nombre, elementos[].nombre, relaciones[].origen, relaciones[].destino, diagrama_mermaid.

Retornar:
{"valid":true,"warnings":[],"errors":[]}
o
{"valid":false,"warnings":["..."],"errors":["descripcion del error"]}

Si el analisis no es JSON valido, retornar:
{"valid":false,"errors":["El analisis recibido no es JSON valido"]}
