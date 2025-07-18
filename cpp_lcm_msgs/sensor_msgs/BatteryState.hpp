/** THIS IS AN AUTOMATICALLY GENERATED FILE.  DO NOT MODIFY
 * BY HAND!!
 *
 * Generated by lcm-gen 1.5.1
 **/

#ifndef __sensor_msgs_BatteryState_hpp__
#define __sensor_msgs_BatteryState_hpp__

#include <lcm/lcm_coretypes.h>

#include <vector>
#include <string>
#include "std_msgs/Header.hpp"

namespace sensor_msgs
{

class BatteryState
{
    public:
        int32_t    cell_voltage_length;

        int32_t    cell_temperature_length;

        std_msgs::Header header;

        float      voltage;

        float      temperature;

        float      current;

        float      charge;

        float      capacity;

        float      design_capacity;

        float      percentage;

        uint8_t    power_supply_status;

        uint8_t    power_supply_health;

        uint8_t    power_supply_technology;

        int8_t     present;

        /**
         * LCM Type: float[cell_voltage_length]
         */
        std::vector< float > cell_voltage;

        /**
         * LCM Type: float[cell_temperature_length]
         */
        std::vector< float > cell_temperature;

        std::string location;

        std::string serial_number;

    public:
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_STATUS_UNKNOWN = 0;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_STATUS_CHARGING = 1;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_STATUS_DISCHARGING = 2;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_STATUS_NOT_CHARGING = 3;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_STATUS_FULL = 4;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_HEALTH_UNKNOWN = 0;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_HEALTH_GOOD = 1;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_HEALTH_OVERHEAT = 2;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_HEALTH_DEAD = 3;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_HEALTH_OVERVOLTAGE = 4;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_HEALTH_UNSPEC_FAILURE = 5;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_HEALTH_COLD = 6;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_HEALTH_WATCHDOG_TIMER_EXPIRE = 7;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_HEALTH_SAFETY_TIMER_EXPIRE = 8;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_TECHNOLOGY_UNKNOWN = 0;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_TECHNOLOGY_NIMH = 1;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_TECHNOLOGY_LION = 2;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_TECHNOLOGY_LIPO = 3;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_TECHNOLOGY_LIFE = 4;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_TECHNOLOGY_NICD = 5;
        // If you're using C++11 and are getting compiler errors saying
        // things like ‘constexpr’ needed for in-class initialization of
        // static data member then re-run lcm-gen with '--cpp-std=c++11'
        // to generate code that is compliant with C++11
        static const int8_t   POWER_SUPPLY_TECHNOLOGY_LIMN = 6;

    public:
        /**
         * Encode a message into binary form.
         *
         * @param buf The output buffer.
         * @param offset Encoding starts at thie byte offset into @p buf.
         * @param maxlen Maximum number of bytes to write.  This should generally be
         *  equal to getEncodedSize().
         * @return The number of bytes encoded, or <0 on error.
         */
        inline int encode(void *buf, int offset, int maxlen) const;

        /**
         * Check how many bytes are required to encode this message.
         */
        inline int getEncodedSize() const;

        /**
         * Decode a message from binary form into this instance.
         *
         * @param buf The buffer containing the encoded message.
         * @param offset The byte offset into @p buf where the encoded message starts.
         * @param maxlen The maximum number of bytes to read while decoding.
         * @return The number of bytes decoded, or <0 if an error occured.
         */
        inline int decode(const void *buf, int offset, int maxlen);

        /**
         * Retrieve the 64-bit fingerprint identifying the structure of the message.
         * Note that the fingerprint is the same for all instances of the same
         * message type, and is a fingerprint on the message type definition, not on
         * the message contents.
         */
        inline static int64_t getHash();

        /**
         * Returns "BatteryState"
         */
        inline static const char* getTypeName();

        // LCM support functions. Users should not call these
        inline int _encodeNoHash(void *buf, int offset, int maxlen) const;
        inline int _getEncodedSizeNoHash() const;
        inline int _decodeNoHash(const void *buf, int offset, int maxlen);
        inline static uint64_t _computeHash(const __lcm_hash_ptr *p);
};

int BatteryState::encode(void *buf, int offset, int maxlen) const
{
    int pos = 0, tlen;
    int64_t hash = getHash();

    tlen = __int64_t_encode_array(buf, offset + pos, maxlen - pos, &hash, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = this->_encodeNoHash(buf, offset + pos, maxlen - pos);
    if (tlen < 0) return tlen; else pos += tlen;

    return pos;
}

int BatteryState::decode(const void *buf, int offset, int maxlen)
{
    int pos = 0, thislen;

    int64_t msg_hash;
    thislen = __int64_t_decode_array(buf, offset + pos, maxlen - pos, &msg_hash, 1);
    if (thislen < 0) return thislen; else pos += thislen;
    if (msg_hash != getHash()) return -1;

    thislen = this->_decodeNoHash(buf, offset + pos, maxlen - pos);
    if (thislen < 0) return thislen; else pos += thislen;

    return pos;
}

int BatteryState::getEncodedSize() const
{
    return 8 + _getEncodedSizeNoHash();
}

int64_t BatteryState::getHash()
{
    static int64_t hash = static_cast<int64_t>(_computeHash(NULL));
    return hash;
}

const char* BatteryState::getTypeName()
{
    return "BatteryState";
}

int BatteryState::_encodeNoHash(void *buf, int offset, int maxlen) const
{
    int pos = 0, tlen;

    tlen = __int32_t_encode_array(buf, offset + pos, maxlen - pos, &this->cell_voltage_length, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __int32_t_encode_array(buf, offset + pos, maxlen - pos, &this->cell_temperature_length, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = this->header._encodeNoHash(buf, offset + pos, maxlen - pos);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_encode_array(buf, offset + pos, maxlen - pos, &this->voltage, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_encode_array(buf, offset + pos, maxlen - pos, &this->temperature, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_encode_array(buf, offset + pos, maxlen - pos, &this->current, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_encode_array(buf, offset + pos, maxlen - pos, &this->charge, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_encode_array(buf, offset + pos, maxlen - pos, &this->capacity, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_encode_array(buf, offset + pos, maxlen - pos, &this->design_capacity, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_encode_array(buf, offset + pos, maxlen - pos, &this->percentage, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __byte_encode_array(buf, offset + pos, maxlen - pos, &this->power_supply_status, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __byte_encode_array(buf, offset + pos, maxlen - pos, &this->power_supply_health, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __byte_encode_array(buf, offset + pos, maxlen - pos, &this->power_supply_technology, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __boolean_encode_array(buf, offset + pos, maxlen - pos, &this->present, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    if(this->cell_voltage_length > 0) {
        tlen = __float_encode_array(buf, offset + pos, maxlen - pos, &this->cell_voltage[0], this->cell_voltage_length);
        if(tlen < 0) return tlen; else pos += tlen;
    }

    if(this->cell_temperature_length > 0) {
        tlen = __float_encode_array(buf, offset + pos, maxlen - pos, &this->cell_temperature[0], this->cell_temperature_length);
        if(tlen < 0) return tlen; else pos += tlen;
    }

    char* location_cstr = const_cast<char*>(this->location.c_str());
    tlen = __string_encode_array(
        buf, offset + pos, maxlen - pos, &location_cstr, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    char* serial_number_cstr = const_cast<char*>(this->serial_number.c_str());
    tlen = __string_encode_array(
        buf, offset + pos, maxlen - pos, &serial_number_cstr, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    return pos;
}

int BatteryState::_decodeNoHash(const void *buf, int offset, int maxlen)
{
    int pos = 0, tlen;

    tlen = __int32_t_decode_array(buf, offset + pos, maxlen - pos, &this->cell_voltage_length, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __int32_t_decode_array(buf, offset + pos, maxlen - pos, &this->cell_temperature_length, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = this->header._decodeNoHash(buf, offset + pos, maxlen - pos);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_decode_array(buf, offset + pos, maxlen - pos, &this->voltage, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_decode_array(buf, offset + pos, maxlen - pos, &this->temperature, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_decode_array(buf, offset + pos, maxlen - pos, &this->current, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_decode_array(buf, offset + pos, maxlen - pos, &this->charge, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_decode_array(buf, offset + pos, maxlen - pos, &this->capacity, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_decode_array(buf, offset + pos, maxlen - pos, &this->design_capacity, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __float_decode_array(buf, offset + pos, maxlen - pos, &this->percentage, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __byte_decode_array(buf, offset + pos, maxlen - pos, &this->power_supply_status, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __byte_decode_array(buf, offset + pos, maxlen - pos, &this->power_supply_health, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __byte_decode_array(buf, offset + pos, maxlen - pos, &this->power_supply_technology, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    tlen = __boolean_decode_array(buf, offset + pos, maxlen - pos, &this->present, 1);
    if(tlen < 0) return tlen; else pos += tlen;

    if(this->cell_voltage_length) {
        this->cell_voltage.resize(this->cell_voltage_length);
        tlen = __float_decode_array(buf, offset + pos, maxlen - pos, &this->cell_voltage[0], this->cell_voltage_length);
        if(tlen < 0) return tlen; else pos += tlen;
    }

    if(this->cell_temperature_length) {
        this->cell_temperature.resize(this->cell_temperature_length);
        tlen = __float_decode_array(buf, offset + pos, maxlen - pos, &this->cell_temperature[0], this->cell_temperature_length);
        if(tlen < 0) return tlen; else pos += tlen;
    }

    int32_t __location_len__;
    tlen = __int32_t_decode_array(
        buf, offset + pos, maxlen - pos, &__location_len__, 1);
    if(tlen < 0) return tlen; else pos += tlen;
    if(__location_len__ > maxlen - pos) return -1;
    this->location.assign(
        static_cast<const char*>(buf) + offset + pos, __location_len__ - 1);
    pos += __location_len__;

    int32_t __serial_number_len__;
    tlen = __int32_t_decode_array(
        buf, offset + pos, maxlen - pos, &__serial_number_len__, 1);
    if(tlen < 0) return tlen; else pos += tlen;
    if(__serial_number_len__ > maxlen - pos) return -1;
    this->serial_number.assign(
        static_cast<const char*>(buf) + offset + pos, __serial_number_len__ - 1);
    pos += __serial_number_len__;

    return pos;
}

int BatteryState::_getEncodedSizeNoHash() const
{
    int enc_size = 0;
    enc_size += __int32_t_encoded_array_size(NULL, 1);
    enc_size += __int32_t_encoded_array_size(NULL, 1);
    enc_size += this->header._getEncodedSizeNoHash();
    enc_size += __float_encoded_array_size(NULL, 1);
    enc_size += __float_encoded_array_size(NULL, 1);
    enc_size += __float_encoded_array_size(NULL, 1);
    enc_size += __float_encoded_array_size(NULL, 1);
    enc_size += __float_encoded_array_size(NULL, 1);
    enc_size += __float_encoded_array_size(NULL, 1);
    enc_size += __float_encoded_array_size(NULL, 1);
    enc_size += __byte_encoded_array_size(NULL, 1);
    enc_size += __byte_encoded_array_size(NULL, 1);
    enc_size += __byte_encoded_array_size(NULL, 1);
    enc_size += __boolean_encoded_array_size(NULL, 1);
    enc_size += __float_encoded_array_size(NULL, this->cell_voltage_length);
    enc_size += __float_encoded_array_size(NULL, this->cell_temperature_length);
    enc_size += this->location.size() + 4 + 1;
    enc_size += this->serial_number.size() + 4 + 1;
    return enc_size;
}

uint64_t BatteryState::_computeHash(const __lcm_hash_ptr *p)
{
    const __lcm_hash_ptr *fp;
    for(fp = p; fp != NULL; fp = fp->parent)
        if(fp->v == BatteryState::getHash)
            return 0;
    const __lcm_hash_ptr cp = { p, (void*)BatteryState::getHash };

    uint64_t hash = 0x8f419fb94c3b774dLL +
         std_msgs::Header::_computeHash(&cp);

    return (hash<<1) + ((hash>>63)&1);
}

}

#endif
