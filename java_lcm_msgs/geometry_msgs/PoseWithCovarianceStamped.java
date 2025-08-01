/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 * lcm-gen 1.5.1
 */

package geometry_msgs;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class PoseWithCovarianceStamped implements lcm.lcm.LCMEncodable
{
    public std_msgs.Header header;

    public geometry_msgs.PoseWithCovariance pose;

 
    public PoseWithCovarianceStamped()
    {
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0xe10feebec5c97663L;
 
    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(geometry_msgs.PoseWithCovarianceStamped.class))
            return 0L;
 
        classes.add(geometry_msgs.PoseWithCovarianceStamped.class);
        long hash = LCM_FINGERPRINT_BASE
             + std_msgs.Header._hashRecursive(classes)
             + geometry_msgs.PoseWithCovariance._hashRecursive(classes)
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
 
        this.pose._encodeRecursive(outs); 
 
    }
 
    public PoseWithCovarianceStamped(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public PoseWithCovarianceStamped(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static geometry_msgs.PoseWithCovarianceStamped _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        geometry_msgs.PoseWithCovarianceStamped o = new geometry_msgs.PoseWithCovarianceStamped();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        this.header = std_msgs.Header._decodeRecursiveFactory(ins);
 
        this.pose = geometry_msgs.PoseWithCovariance._decodeRecursiveFactory(ins);
 
    }
 
    public geometry_msgs.PoseWithCovarianceStamped copy()
    {
        geometry_msgs.PoseWithCovarianceStamped outobj = new geometry_msgs.PoseWithCovarianceStamped();
        outobj.header = this.header.copy();
 
        outobj.pose = this.pose.copy();
 
        return outobj;
    }
 
}

