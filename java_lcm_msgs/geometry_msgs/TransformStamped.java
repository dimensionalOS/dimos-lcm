/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 * lcm-gen 1.5.1
 */

package geometry_msgs;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class TransformStamped implements lcm.lcm.LCMEncodable
{
    public std_msgs.Header header;

    public String child_frame_id;

    public geometry_msgs.Transform transform;

 
    public TransformStamped()
    {
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0xf694f4a6d8779002L;
 
    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(geometry_msgs.TransformStamped.class))
            return 0L;
 
        classes.add(geometry_msgs.TransformStamped.class);
        long hash = LCM_FINGERPRINT_BASE
             + std_msgs.Header._hashRecursive(classes)
             + geometry_msgs.Transform._hashRecursive(classes)
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
        char[] __strbuf = null;
        this.header._encodeRecursive(outs); 
 
        __strbuf = new char[this.child_frame_id.length()]; this.child_frame_id.getChars(0, this.child_frame_id.length(), __strbuf, 0); outs.writeInt(__strbuf.length+1); for (int _i = 0; _i < __strbuf.length; _i++) outs.write(__strbuf[_i]); outs.writeByte(0); 
 
        this.transform._encodeRecursive(outs); 
 
    }
 
    public TransformStamped(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public TransformStamped(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static geometry_msgs.TransformStamped _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        geometry_msgs.TransformStamped o = new geometry_msgs.TransformStamped();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        char[] __strbuf = null;
        this.header = std_msgs.Header._decodeRecursiveFactory(ins);
 
        __strbuf = new char[ins.readInt()-1]; for (int _i = 0; _i < __strbuf.length; _i++) __strbuf[_i] = (char) (ins.readByte()&0xff); ins.readByte(); this.child_frame_id = new String(__strbuf);
 
        this.transform = geometry_msgs.Transform._decodeRecursiveFactory(ins);
 
    }
 
    public geometry_msgs.TransformStamped copy()
    {
        geometry_msgs.TransformStamped outobj = new geometry_msgs.TransformStamped();
        outobj.header = this.header.copy();
 
        outobj.child_frame_id = this.child_frame_id;
 
        outobj.transform = this.transform.copy();
 
        return outobj;
    }
 
}

