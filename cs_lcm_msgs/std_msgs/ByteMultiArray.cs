/* LCM type definition class file
 * This file was automatically generated by lcm-gen 1.5.1
 * DO NOT MODIFY BY HAND!!!!
 */

using System;
using System.Collections.Generic;
using System.IO;
using LCM.LCM;
 
namespace std_msgs
{
    public sealed class ByteMultiArray : LCM.LCM.LCMEncodable
    {
        public int data_length;
        public std_msgs.MultiArrayLayout layout;
        public sbyte[] data;
 
        public ByteMultiArray()
        {
        }
 
        public static readonly ulong LCM_FINGERPRINT;
        public static readonly ulong LCM_FINGERPRINT_BASE = 0xdcc1940b891be505L;
 
        static ByteMultiArray()
        {
            LCM_FINGERPRINT = _hashRecursive(new List<String>());
        }
 
        public static ulong _hashRecursive(List<String> classes)
        {
            if (classes.Contains("std_msgs.ByteMultiArray"))
                return 0L;
 
            classes.Add("std_msgs.ByteMultiArray");
            ulong hash = LCM_FINGERPRINT_BASE
                 + std_msgs.MultiArrayLayout._hashRecursive(classes)
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
            outs.Write(this.data_length); 
 
            this.layout._encodeRecursive(outs); 
 
            for (int a = 0; a < this.data_length; a++) {
                outs.Write(this.data[a]); 
            }
 
        }
 
        public ByteMultiArray(byte[] data) : this(new LCMDataInputStream(data))
        {
        }
 
        public ByteMultiArray(LCMDataInputStream ins)
        {
            if ((ulong) ins.ReadInt64() != LCM_FINGERPRINT)
                throw new System.IO.IOException("LCM Decode error: bad fingerprint");
 
            _decodeRecursive(ins);
        }
 
        public static std_msgs.ByteMultiArray _decodeRecursiveFactory(LCMDataInputStream ins)
        {
            std_msgs.ByteMultiArray o = new std_msgs.ByteMultiArray();
            o._decodeRecursive(ins);
            return o;
        }
 
        public void _decodeRecursive(LCMDataInputStream ins)
        {
            this.data_length = ins.ReadInt32();
 
            this.layout = std_msgs.MultiArrayLayout._decodeRecursiveFactory(ins);
 
            this.data = new sbyte[(int) data_length];
            for (int a = 0; a < this.data_length; a++) {
                this.data[a] = ins.ReadSByte();
            }
 
        }
 
        public std_msgs.ByteMultiArray Copy()
        {
            std_msgs.ByteMultiArray outobj = new std_msgs.ByteMultiArray();
            outobj.data_length = this.data_length;
 
            outobj.layout = this.layout.Copy();
 
            outobj.data = new sbyte[(int) data_length];
            for (int a = 0; a < this.data_length; a++) {
                outobj.data[a] = this.data[a];
            }
 
            return outobj;
        }
    }
}

