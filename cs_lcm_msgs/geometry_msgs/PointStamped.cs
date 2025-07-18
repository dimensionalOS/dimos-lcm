/* LCM type definition class file
 * This file was automatically generated by lcm-gen 1.5.1
 * DO NOT MODIFY BY HAND!!!!
 */

using System;
using System.Collections.Generic;
using System.IO;
using LCM.LCM;
 
namespace geometry_msgs
{
    public sealed class PointStamped : LCM.LCM.LCMEncodable
    {
        public std_msgs.Header header;
        public geometry_msgs.Point point;
 
        public PointStamped()
        {
        }
 
        public static readonly ulong LCM_FINGERPRINT;
        public static readonly ulong LCM_FINGERPRINT_BASE = 0xf012413a2c8028c2L;
 
        static PointStamped()
        {
            LCM_FINGERPRINT = _hashRecursive(new List<String>());
        }
 
        public static ulong _hashRecursive(List<String> classes)
        {
            if (classes.Contains("geometry_msgs.PointStamped"))
                return 0L;
 
            classes.Add("geometry_msgs.PointStamped");
            ulong hash = LCM_FINGERPRINT_BASE
                 + std_msgs.Header._hashRecursive(classes)
                 + geometry_msgs.Point._hashRecursive(classes)
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
 
            this.point._encodeRecursive(outs); 
 
        }
 
        public PointStamped(byte[] data) : this(new LCMDataInputStream(data))
        {
        }
 
        public PointStamped(LCMDataInputStream ins)
        {
            if ((ulong) ins.ReadInt64() != LCM_FINGERPRINT)
                throw new System.IO.IOException("LCM Decode error: bad fingerprint");
 
            _decodeRecursive(ins);
        }
 
        public static geometry_msgs.PointStamped _decodeRecursiveFactory(LCMDataInputStream ins)
        {
            geometry_msgs.PointStamped o = new geometry_msgs.PointStamped();
            o._decodeRecursive(ins);
            return o;
        }
 
        public void _decodeRecursive(LCMDataInputStream ins)
        {
            this.header = std_msgs.Header._decodeRecursiveFactory(ins);
 
            this.point = geometry_msgs.Point._decodeRecursiveFactory(ins);
 
        }
 
        public geometry_msgs.PointStamped Copy()
        {
            geometry_msgs.PointStamped outobj = new geometry_msgs.PointStamped();
            outobj.header = this.header.Copy();
 
            outobj.point = this.point.Copy();
 
            return outobj;
        }
    }
}

