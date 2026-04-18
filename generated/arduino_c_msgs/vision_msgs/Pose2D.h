/*
 * vision_msgs/Pose2D — Arduino-compatible LCM C encode/decode.
 * Wire format: Point2D(16) + double = 24 bytes.
 */
#ifndef DIMOS_ARDUINO_MSG_POSE2D_H
#define DIMOS_ARDUINO_MSG_POSE2D_H

#include "vision_msgs/Point2D.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    dimos_msg__Point2D position;
    double theta;
} dimos_msg__Pose2D;

static inline int dimos_msg__Pose2D__encoded_size(void) { return 24; }

static inline int dimos_msg__Pose2D__encode(void *buf, int offset, int maxlen,
    const dimos_msg__Pose2D *p)
{
    int pos = 0, thislen;
    thislen = dimos_msg__Point2D__encode(buf, offset + pos, maxlen - pos, &p->position);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __double_encode_array(buf, offset + pos, maxlen - pos, &p->theta, 1);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

static inline int dimos_msg__Pose2D__decode(const void *buf, int offset,
    int maxlen, dimos_msg__Pose2D *p)
{
    int pos = 0, thislen;
    thislen = dimos_msg__Point2D__decode(buf, offset + pos, maxlen - pos, &p->position);
    if (thislen < 0) return thislen; pos += thislen;
    thislen = __double_decode_array(buf, offset + pos, maxlen - pos, &p->theta, 1);
    if (thislen < 0) return thislen; pos += thislen;
    return pos;
}

#ifdef __cplusplus
}
#endif

#endif
