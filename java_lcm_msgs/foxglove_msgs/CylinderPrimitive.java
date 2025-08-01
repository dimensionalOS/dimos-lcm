/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 * lcm-gen 1.5.1
 */

package foxglove_msgs;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class CylinderPrimitive implements lcm.lcm.LCMEncodable
{
    public geometry_msgs.Pose pose;

    public geometry_msgs.Vector3 size;

    public double bottom_scale;

    public double top_scale;

    public foxglove_msgs.Color color;

 
    public CylinderPrimitive()
    {
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0xa52103034bfe0bacL;
 
    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(foxglove_msgs.CylinderPrimitive.class))
            return 0L;
 
        classes.add(foxglove_msgs.CylinderPrimitive.class);
        long hash = LCM_FINGERPRINT_BASE
             + geometry_msgs.Pose._hashRecursive(classes)
             + geometry_msgs.Vector3._hashRecursive(classes)
             + foxglove_msgs.Color._hashRecursive(classes)
            ;
        classes.remove(classes.size() - 1);
        return (hash<<1) + ((hash>>63)&1);
    }
 
    public void encode(DataOutput outs) throws IOException
    {
        outs.writeLong(LCM_FINGERPRINT);
        _encodeRecursive(outs);
    }
 
    public void _encodeRecursive(DataOutput outs) throws IOException
    {
        this.pose._encodeRecursive(outs); 
 
        this.size._encodeRecursive(outs); 
 
        outs.writeDouble(this.bottom_scale); 
 
        outs.writeDouble(this.top_scale); 
 
        this.color._encodeRecursive(outs); 
 
    }
 
    public CylinderPrimitive(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public CylinderPrimitive(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static foxglove_msgs.CylinderPrimitive _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        foxglove_msgs.CylinderPrimitive o = new foxglove_msgs.CylinderPrimitive();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        this.pose = geometry_msgs.Pose._decodeRecursiveFactory(ins);
 
        this.size = geometry_msgs.Vector3._decodeRecursiveFactory(ins);
 
        this.bottom_scale = ins.readDouble();
 
        this.top_scale = ins.readDouble();
 
        this.color = foxglove_msgs.Color._decodeRecursiveFactory(ins);
 
    }
 
    public foxglove_msgs.CylinderPrimitive copy()
    {
        foxglove_msgs.CylinderPrimitive outobj = new foxglove_msgs.CylinderPrimitive();
        outobj.pose = this.pose.copy();
 
        outobj.size = this.size.copy();
 
        outobj.bottom_scale = this.bottom_scale;
 
        outobj.top_scale = this.top_scale;
 
        outobj.color = this.color.copy();
 
        return outobj;
    }
 
}

