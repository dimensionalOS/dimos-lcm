/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 * lcm-gen 1.5.1
 */

package geometry_msgs;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class AccelWithCovarianceStamped implements lcm.lcm.LCMEncodable
{
    public std_msgs.Header header;

    public geometry_msgs.AccelWithCovariance accel;

 
    public AccelWithCovarianceStamped()
    {
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0xf012322e268930c2L;
 
    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(geometry_msgs.AccelWithCovarianceStamped.class))
            return 0L;
 
        classes.add(geometry_msgs.AccelWithCovarianceStamped.class);
        long hash = LCM_FINGERPRINT_BASE
             + std_msgs.Header._hashRecursive(classes)
             + geometry_msgs.AccelWithCovariance._hashRecursive(classes)
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
 
        this.accel._encodeRecursive(outs); 
 
    }
 
    public AccelWithCovarianceStamped(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public AccelWithCovarianceStamped(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static geometry_msgs.AccelWithCovarianceStamped _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        geometry_msgs.AccelWithCovarianceStamped o = new geometry_msgs.AccelWithCovarianceStamped();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        this.header = std_msgs.Header._decodeRecursiveFactory(ins);
 
        this.accel = geometry_msgs.AccelWithCovariance._decodeRecursiveFactory(ins);
 
    }
 
    public geometry_msgs.AccelWithCovarianceStamped copy()
    {
        geometry_msgs.AccelWithCovarianceStamped outobj = new geometry_msgs.AccelWithCovarianceStamped();
        outobj.header = this.header.copy();
 
        outobj.accel = this.accel.copy();
 
        return outobj;
    }
 
}

