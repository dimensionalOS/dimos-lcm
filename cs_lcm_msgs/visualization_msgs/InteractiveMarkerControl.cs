/* LCM type definition class file
 * This file was automatically generated by lcm-gen 1.5.1
 * DO NOT MODIFY BY HAND!!!!
 */

using System;
using System.Collections.Generic;
using System.IO;
using LCM.LCM;
 
namespace visualization_msgs
{
    public sealed class InteractiveMarkerControl : LCM.LCM.LCMEncodable
    {
        public int markers_length;
        public String name;
        public geometry_msgs.Quaternion orientation;
        public byte orientation_mode;
        public byte interaction_mode;
        public bool always_visible;
        public visualization_msgs.Marker[] markers;
        public bool independent_marker_orientation;
        public String description;
 
        public InteractiveMarkerControl()
        {
        }
 
        public static readonly ulong LCM_FINGERPRINT;
        public static readonly ulong LCM_FINGERPRINT_BASE = 0x9e1db7d7740da609L;
 
        public const int INHERIT = 0;
        public const int FIXED = 1;
        public const int VIEW_FACING = 2;
        public const int NONE = 0;
        public const int MENU = 1;
        public const int BUTTON = 2;
        public const int MOVE_AXIS = 3;
        public const int MOVE_PLANE = 4;
        public const int ROTATE_AXIS = 5;
        public const int MOVE_ROTATE = 6;
        public const int MOVE_3D = 7;
        public const int ROTATE_3D = 8;
        public const int MOVE_ROTATE_3D = 9;

        static InteractiveMarkerControl()
        {
            LCM_FINGERPRINT = _hashRecursive(new List<String>());
        }
 
        public static ulong _hashRecursive(List<String> classes)
        {
            if (classes.Contains("visualization_msgs.InteractiveMarkerControl"))
                return 0L;
 
            classes.Add("visualization_msgs.InteractiveMarkerControl");
            ulong hash = LCM_FINGERPRINT_BASE
                 + geometry_msgs.Quaternion._hashRecursive(classes)
                 + visualization_msgs.Marker._hashRecursive(classes)
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
            outs.Write(this.markers_length); 
 
            __strbuf = System.Text.Encoding.GetEncoding("US-ASCII").GetBytes(this.name); outs.Write(__strbuf.Length+1); outs.Write(__strbuf, 0, __strbuf.Length); outs.Write((byte) 0); 
 
            this.orientation._encodeRecursive(outs); 
 
            outs.Write(this.orientation_mode); 
 
            outs.Write(this.interaction_mode); 
 
            outs.Write(this.always_visible); 
 
            for (int a = 0; a < this.markers_length; a++) {
                this.markers[a]._encodeRecursive(outs); 
            }
 
            outs.Write(this.independent_marker_orientation); 
 
            __strbuf = System.Text.Encoding.GetEncoding("US-ASCII").GetBytes(this.description); outs.Write(__strbuf.Length+1); outs.Write(__strbuf, 0, __strbuf.Length); outs.Write((byte) 0); 
 
        }
 
        public InteractiveMarkerControl(byte[] data) : this(new LCMDataInputStream(data))
        {
        }
 
        public InteractiveMarkerControl(LCMDataInputStream ins)
        {
            if ((ulong) ins.ReadInt64() != LCM_FINGERPRINT)
                throw new System.IO.IOException("LCM Decode error: bad fingerprint");
 
            _decodeRecursive(ins);
        }
 
        public static visualization_msgs.InteractiveMarkerControl _decodeRecursiveFactory(LCMDataInputStream ins)
        {
            visualization_msgs.InteractiveMarkerControl o = new visualization_msgs.InteractiveMarkerControl();
            o._decodeRecursive(ins);
            return o;
        }
 
        public void _decodeRecursive(LCMDataInputStream ins)
        {
            byte[] __strbuf = null;
            this.markers_length = ins.ReadInt32();
 
            __strbuf = new byte[ins.ReadInt32()-1]; ins.ReadFully(__strbuf); ins.ReadByte(); this.name = System.Text.Encoding.GetEncoding("US-ASCII").GetString(__strbuf);
 
            this.orientation = geometry_msgs.Quaternion._decodeRecursiveFactory(ins);
 
            this.orientation_mode = ins.ReadByte();
 
            this.interaction_mode = ins.ReadByte();
 
            this.always_visible = ins.ReadBoolean();
 
            this.markers = new visualization_msgs.Marker[(int) markers_length];
            for (int a = 0; a < this.markers_length; a++) {
                this.markers[a] = visualization_msgs.Marker._decodeRecursiveFactory(ins);
            }
 
            this.independent_marker_orientation = ins.ReadBoolean();
 
            __strbuf = new byte[ins.ReadInt32()-1]; ins.ReadFully(__strbuf); ins.ReadByte(); this.description = System.Text.Encoding.GetEncoding("US-ASCII").GetString(__strbuf);
 
        }
 
        public visualization_msgs.InteractiveMarkerControl Copy()
        {
            visualization_msgs.InteractiveMarkerControl outobj = new visualization_msgs.InteractiveMarkerControl();
            outobj.markers_length = this.markers_length;
 
            outobj.name = this.name;
 
            outobj.orientation = this.orientation.Copy();
 
            outobj.orientation_mode = this.orientation_mode;
 
            outobj.interaction_mode = this.interaction_mode;
 
            outobj.always_visible = this.always_visible;
 
            outobj.markers = new visualization_msgs.Marker[(int) markers_length];
            for (int a = 0; a < this.markers_length; a++) {
                outobj.markers[a] = this.markers[a].Copy();
            }
 
            outobj.independent_marker_orientation = this.independent_marker_orientation;
 
            outobj.description = this.description;
 
            return outobj;
        }
    }
}

