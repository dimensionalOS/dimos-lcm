/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 * lcm-gen 1.5.1
 */

package foxglove_msgs;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class SceneEntityDeletion implements lcm.lcm.LCMEncodable
{
    public builtin_interfaces.Time timestamp;

    public byte type;

    public String id;

 
    public SceneEntityDeletion()
    {
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0xa6b01fa4694da548L;
 
    public static final byte MATCHING_ID = (byte) 0;
    public static final byte ALL = (byte) 1;

    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(foxglove_msgs.SceneEntityDeletion.class))
            return 0L;
 
        classes.add(foxglove_msgs.SceneEntityDeletion.class);
        long hash = LCM_FINGERPRINT_BASE
             + builtin_interfaces.Time._hashRecursive(classes)
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
 
        outs.writeByte(this.type); 
 
        __strbuf = new char[this.id.length()]; this.id.getChars(0, this.id.length(), __strbuf, 0); outs.writeInt(__strbuf.length+1); for (int _i = 0; _i < __strbuf.length; _i++) outs.write(__strbuf[_i]); outs.writeByte(0); 
 
    }
 
    public SceneEntityDeletion(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public SceneEntityDeletion(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static foxglove_msgs.SceneEntityDeletion _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        foxglove_msgs.SceneEntityDeletion o = new foxglove_msgs.SceneEntityDeletion();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        char[] __strbuf = null;
        this.timestamp = builtin_interfaces.Time._decodeRecursiveFactory(ins);
 
        this.type = ins.readByte();
 
        __strbuf = new char[ins.readInt()-1]; for (int _i = 0; _i < __strbuf.length; _i++) __strbuf[_i] = (char) (ins.readByte()&0xff); ins.readByte(); this.id = new String(__strbuf);
 
    }
 
    public foxglove_msgs.SceneEntityDeletion copy()
    {
        foxglove_msgs.SceneEntityDeletion outobj = new foxglove_msgs.SceneEntityDeletion();
        outobj.timestamp = this.timestamp.copy();
 
        outobj.type = this.type;
 
        outobj.id = this.id;
 
        return outobj;
    }
 
}

