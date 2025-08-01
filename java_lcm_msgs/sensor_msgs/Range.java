/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 * lcm-gen 1.5.1
 */

package sensor_msgs;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class Range implements lcm.lcm.LCMEncodable
{
    public std_msgs.Header header;

    public byte radiation_type;

    public float field_of_view;

    public float min_range;

    public float max_range;

    public float range;

 
    public Range()
    {
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0xaaf9249a1465f86aL;
 
    public static final byte ULTRASOUND = (byte) 0;
    public static final byte INFRARED = (byte) 1;

    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(sensor_msgs.Range.class))
            return 0L;
 
        classes.add(sensor_msgs.Range.class);
        long hash = LCM_FINGERPRINT_BASE
             + std_msgs.Header._hashRecursive(classes)
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
        this.header._encodeRecursive(outs); 
 
        outs.writeByte(this.radiation_type); 
 
        outs.writeFloat(this.field_of_view); 
 
        outs.writeFloat(this.min_range); 
 
        outs.writeFloat(this.max_range); 
 
        outs.writeFloat(this.range); 
 
    }
 
    public Range(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public Range(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static sensor_msgs.Range _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        sensor_msgs.Range o = new sensor_msgs.Range();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        this.header = std_msgs.Header._decodeRecursiveFactory(ins);
 
        this.radiation_type = ins.readByte();
 
        this.field_of_view = ins.readFloat();
 
        this.min_range = ins.readFloat();
 
        this.max_range = ins.readFloat();
 
        this.range = ins.readFloat();
 
    }
 
    public sensor_msgs.Range copy()
    {
        sensor_msgs.Range outobj = new sensor_msgs.Range();
        outobj.header = this.header.copy();
 
        outobj.radiation_type = this.radiation_type;
 
        outobj.field_of_view = this.field_of_view;
 
        outobj.min_range = this.min_range;
 
        outobj.max_range = this.max_range;
 
        outobj.range = this.range;
 
        return outobj;
    }
 
}

