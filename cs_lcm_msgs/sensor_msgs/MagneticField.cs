/* LCM type definition class file
 * This file was automatically generated by lcm-gen 1.5.1
 * DO NOT MODIFY BY HAND!!!!
 */

using System;
using System.Collections.Generic;
using System.IO;
using LCM.LCM;
 
namespace sensor_msgs
{
    public sealed class MagneticField : LCM.LCM.LCMEncodable
    {
        public std_msgs.Header header;
        public geometry_msgs.Vector3 magnetic_field;
        public double[] magnetic_field_covariance;
 
        public MagneticField()
        {
            magnetic_field_covariance = new double[9];
        }
 
        public static readonly ulong LCM_FINGERPRINT;
        public static readonly ulong LCM_FINGERPRINT_BASE = 0xbfeb021e4751ed88L;
 
        static MagneticField()
        {
            LCM_FINGERPRINT = _hashRecursive(new List<String>());
        }
 
        public static ulong _hashRecursive(List<String> classes)
        {
            if (classes.Contains("sensor_msgs.MagneticField"))
                return 0L;
 
            classes.Add("sensor_msgs.MagneticField");
            ulong hash = LCM_FINGERPRINT_BASE
                 + std_msgs.Header._hashRecursive(classes)
                 + geometry_msgs.Vector3._hashRecursive(classes)
                ;
            classes.RemoveAt(classes.Count - 1);
            return (hash<<1) + ((hash>>63)&1);
        }
 
        public void Encode(LCMDataOutputStream outs)
        {
            outs.Write((long) LCM_FINGERPRINT);
            _encodeRecursive(outs);
        }
 
        public void _encodeRecursive(LCMDataOutputStream outs)
        {
            this.header._encodeRecursive(outs); 
 
            this.magnetic_field._encodeRecursive(outs); 
 
            for (int a = 0; a < 9; a++) {
                outs.Write(this.magnetic_field_covariance[a]); 
            }
 
        }
 
        public MagneticField(byte[] data) : this(new LCMDataInputStream(data))
        {
        }
 
        public MagneticField(LCMDataInputStream ins)
        {
            if ((ulong) ins.ReadInt64() != LCM_FINGERPRINT)
                throw new System.IO.IOException("LCM Decode error: bad fingerprint");
 
            _decodeRecursive(ins);
        }
 
        public static sensor_msgs.MagneticField _decodeRecursiveFactory(LCMDataInputStream ins)
        {
            sensor_msgs.MagneticField o = new sensor_msgs.MagneticField();
            o._decodeRecursive(ins);
            return o;
        }
 
        public void _decodeRecursive(LCMDataInputStream ins)
        {
            this.header = std_msgs.Header._decodeRecursiveFactory(ins);
 
            this.magnetic_field = geometry_msgs.Vector3._decodeRecursiveFactory(ins);
 
            this.magnetic_field_covariance = new double[(int) 9];
            for (int a = 0; a < 9; a++) {
                this.magnetic_field_covariance[a] = ins.ReadDouble();
            }
 
        }
 
        public sensor_msgs.MagneticField Copy()
        {
            sensor_msgs.MagneticField outobj = new sensor_msgs.MagneticField();
            outobj.header = this.header.Copy();
 
            outobj.magnetic_field = this.magnetic_field.Copy();
 
            outobj.magnetic_field_covariance = new double[(int) 9];
            for (int a = 0; a < 9; a++) {
                outobj.magnetic_field_covariance[a] = this.magnetic_field_covariance[a];
            }
 
            return outobj;
        }
    }
}

