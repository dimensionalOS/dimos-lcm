/* LCM type definition class file
 * This file was automatically generated by lcm-gen 1.5.1
 * DO NOT MODIFY BY HAND!!!!
 */

using System;
using System.Collections.Generic;
using System.IO;
using LCM.LCM;
 
namespace foxglove_msgs
{
    public sealed class PointCloud : LCM.LCM.LCMEncodable
    {
        public int fields_length;
        public int data_length;
        public builtin_interfaces.Time timestamp;
        public String frame_id;
        public geometry_msgs.Pose pose;
        public int point_stride;
        public foxglove_msgs.PackedElementField[] fields;
        public byte[] data;
 
        public PointCloud()
        {
        }
 
        public static readonly ulong LCM_FINGERPRINT;
        public static readonly ulong LCM_FINGERPRINT_BASE = 0x4f3713aa9b8dc878L;
 
        static PointCloud()
        {
            LCM_FINGERPRINT = _hashRecursive(new List<String>());
        }
 
        public static ulong _hashRecursive(List<String> classes)
        {
            if (classes.Contains("foxglove_msgs.PointCloud"))
                return 0L;
 
            classes.Add("foxglove_msgs.PointCloud");
            ulong hash = LCM_FINGERPRINT_BASE
                 + builtin_interfaces.Time._hashRecursive(classes)
                 + geometry_msgs.Pose._hashRecursive(classes)
                 + foxglove_msgs.PackedElementField._hashRecursive(classes)
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
            byte[] __strbuf = null;
            outs.Write(this.fields_length); 
 
            outs.Write(this.data_length); 
 
            this.timestamp._encodeRecursive(outs); 
 
            __strbuf = System.Text.Encoding.GetEncoding("US-ASCII").GetBytes(this.frame_id); outs.Write(__strbuf.Length+1); outs.Write(__strbuf, 0, __strbuf.Length); outs.Write((byte) 0); 
 
            this.pose._encodeRecursive(outs); 
 
            outs.Write(this.point_stride); 
 
            for (int a = 0; a < this.fields_length; a++) {
                this.fields[a]._encodeRecursive(outs); 
            }
 
            for (int a = 0; a < this.data_length; a++) {
                outs.Write(this.data[a]); 
            }
 
        }
 
        public PointCloud(byte[] data) : this(new LCMDataInputStream(data))
        {
        }
 
        public PointCloud(LCMDataInputStream ins)
        {
            if ((ulong) ins.ReadInt64() != LCM_FINGERPRINT)
                throw new System.IO.IOException("LCM Decode error: bad fingerprint");
 
            _decodeRecursive(ins);
        }
 
        public static foxglove_msgs.PointCloud _decodeRecursiveFactory(LCMDataInputStream ins)
        {
            foxglove_msgs.PointCloud o = new foxglove_msgs.PointCloud();
            o._decodeRecursive(ins);
            return o;
        }
 
        public void _decodeRecursive(LCMDataInputStream ins)
        {
            byte[] __strbuf = null;
            this.fields_length = ins.ReadInt32();
 
            this.data_length = ins.ReadInt32();
 
            this.timestamp = builtin_interfaces.Time._decodeRecursiveFactory(ins);
 
            __strbuf = new byte[ins.ReadInt32()-1]; ins.ReadFully(__strbuf); ins.ReadByte(); this.frame_id = System.Text.Encoding.GetEncoding("US-ASCII").GetString(__strbuf);
 
            this.pose = geometry_msgs.Pose._decodeRecursiveFactory(ins);
 
            this.point_stride = ins.ReadInt32();
 
            this.fields = new foxglove_msgs.PackedElementField[(int) fields_length];
            for (int a = 0; a < this.fields_length; a++) {
                this.fields[a] = foxglove_msgs.PackedElementField._decodeRecursiveFactory(ins);
            }
 
            this.data = new byte[(int) data_length];
            for (int a = 0; a < this.data_length; a++) {
                this.data[a] = ins.ReadByte();
            }
 
        }
 
        public foxglove_msgs.PointCloud Copy()
        {
            foxglove_msgs.PointCloud outobj = new foxglove_msgs.PointCloud();
            outobj.fields_length = this.fields_length;
 
            outobj.data_length = this.data_length;
 
            outobj.timestamp = this.timestamp.Copy();
 
            outobj.frame_id = this.frame_id;
 
            outobj.pose = this.pose.Copy();
 
            outobj.point_stride = this.point_stride;
 
            outobj.fields = new foxglove_msgs.PackedElementField[(int) fields_length];
            for (int a = 0; a < this.fields_length; a++) {
                outobj.fields[a] = this.fields[a].Copy();
            }
 
            outobj.data = new byte[(int) data_length];
            for (int a = 0; a < this.data_length; a++) {
                outobj.data[a] = this.data[a];
            }
 
            return outobj;
        }
    }
}

