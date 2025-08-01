/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 * lcm-gen 1.5.1
 */

package foxglove_msgs;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class PoseInFrame implements lcm.lcm.LCMEncodable
{
    public builtin_interfaces.Time timestamp;

    public String frame_id;

    public geometry_msgs.Pose pose;

 
    public PoseInFrame()
    {
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0x84c6ef3a0a4c5cd6L;
 
    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(foxglove_msgs.PoseInFrame.class))
            return 0L;
 
        classes.add(foxglove_msgs.PoseInFrame.class);
        long hash = LCM_FINGERPRINT_BASE
             + builtin_interfaces.Time._hashRecursive(classes)
             + geometry_msgs.Pose._hashRecursive(classes)
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
        this.timestamp._encodeRecursive(outs); 
 
        __strbuf = new char[this.frame_id.length()]; this.frame_id.getChars(0, this.frame_id.length(), __strbuf, 0); outs.writeInt(__strbuf.length+1); for (int _i = 0; _i < __strbuf.length; _i++) outs.write(__strbuf[_i]); outs.writeByte(0); 
 
        this.pose._encodeRecursive(outs); 
 
    }
 
    public PoseInFrame(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public PoseInFrame(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static foxglove_msgs.PoseInFrame _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        foxglove_msgs.PoseInFrame o = new foxglove_msgs.PoseInFrame();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        char[] __strbuf = null;
        this.timestamp = builtin_interfaces.Time._decodeRecursiveFactory(ins);
 
        __strbuf = new char[ins.readInt()-1]; for (int _i = 0; _i < __strbuf.length; _i++) __strbuf[_i] = (char) (ins.readByte()&0xff); ins.readByte(); this.frame_id = new String(__strbuf);
 
        this.pose = geometry_msgs.Pose._decodeRecursiveFactory(ins);
 
    }
 
    public foxglove_msgs.PoseInFrame copy()
    {
        foxglove_msgs.PoseInFrame outobj = new foxglove_msgs.PoseInFrame();
        outobj.timestamp = this.timestamp.copy();
 
        outobj.frame_id = this.frame_id;
 
        outobj.pose = this.pose.copy();
 
        return outobj;
    }
 
}

