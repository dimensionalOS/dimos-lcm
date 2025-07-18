/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 * lcm-gen 1.5.1
 */

package geometry_msgs;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class TwistWithCovariance implements lcm.lcm.LCMEncodable
{
    public geometry_msgs.Twist twist;

    /**
     * LCM Type: double[36]
     */
    public double covariance[];

 
    public TwistWithCovariance()
    {
        covariance = new double[36];
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0xaba0a9d55e98da5dL;
 
    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(geometry_msgs.TwistWithCovariance.class))
            return 0L;
 
        classes.add(geometry_msgs.TwistWithCovariance.class);
        long hash = LCM_FINGERPRINT_BASE
             + geometry_msgs.Twist._hashRecursive(classes)
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
        this.twist._encodeRecursive(outs); 
 
        for (int a = 0; a < 36; a++) {
            outs.writeDouble(this.covariance[a]); 
        }
 
    }
 
    public TwistWithCovariance(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public TwistWithCovariance(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static geometry_msgs.TwistWithCovariance _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        geometry_msgs.TwistWithCovariance o = new geometry_msgs.TwistWithCovariance();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        this.twist = geometry_msgs.Twist._decodeRecursiveFactory(ins);
 
        this.covariance = new double[(int) 36];
        for (int a = 0; a < 36; a++) {
            this.covariance[a] = ins.readDouble();
        }
 
    }
 
    public geometry_msgs.TwistWithCovariance copy()
    {
        geometry_msgs.TwistWithCovariance outobj = new geometry_msgs.TwistWithCovariance();
        outobj.twist = this.twist.copy();
 
        outobj.covariance = new double[(int) 36];
        System.arraycopy(this.covariance, 0, outobj.covariance, 0, 36); 
        return outobj;
    }
 
}

