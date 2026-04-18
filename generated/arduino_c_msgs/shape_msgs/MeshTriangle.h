/*
 * shape_msgs/MeshTriangle — Arduino-compatible LCM C encode/decode.
 * Wire format: 3x int32_t(12) = 12 bytes.
 */
#ifndef DIMOS_ARDUINO_MSG_MESHTRIANGLE_H
#define DIMOS_ARDUINO_MSG_MESHTRIANGLE_H

#include "lcm_coretypes_arduino.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    int32_t vertex_indices[3];
} dimos_msg__MeshTriangle;

static inline int dimos_msg__MeshTriangle__encoded_size(void) { return 12; }

static inline int dimos_msg__MeshTriangle__encode(void *buf, int offset, int maxlen,
    const dimos_msg__MeshTriangle *p)
{
    int pos = 0, thislen;
    thislen = __int32_t_encode_array(buf, offset + pos, maxlen - pos, p->vertex_indices, 3);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

static inline int dimos_msg__MeshTriangle__decode(const void *buf, int offset,
    int maxlen, dimos_msg__MeshTriangle *p)
{
    int pos = 0, thislen;
    thislen = __int32_t_decode_array(buf, offset + pos, maxlen - pos, p->vertex_indices, 3);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

#ifdef __cplusplus
}
#endif

#endif
