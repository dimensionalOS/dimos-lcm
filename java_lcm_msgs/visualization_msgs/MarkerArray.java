/* LCM type definition class file
 * This file was automatically generated by lcm-gen
 * DO NOT MODIFY BY HAND!!!!
 * lcm-gen 1.5.1
 */

package visualization_msgs;
 
import java.io.*;
import java.util.*;
import lcm.lcm.*;
 
public final class MarkerArray implements lcm.lcm.LCMEncodable
{
    public int markers_length;

    /**
     * LCM Type: visualization_msgs.Marker[markers_length]
     */
    public visualization_msgs.Marker markers[];

 
    public MarkerArray()
    {
    }
 
    public static final long LCM_FINGERPRINT;
    public static final long LCM_FINGERPRINT_BASE = 0xd9e3851dad1e0d9eL;
 
    static {
        LCM_FINGERPRINT = _hashRecursive(new ArrayList<Class<?>>());
    }
 
    public static long _hashRecursive(ArrayList<Class<?>> classes)
    {
        if (classes.contains(visualization_msgs.MarkerArray.class))
            return 0L;
 
        classes.add(visualization_msgs.MarkerArray.class);
        long hash = LCM_FINGERPRINT_BASE
             + visualization_msgs.Marker._hashRecursive(classes)
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
        outs.writeInt(this.markers_length); 
 
        for (int a = 0; a < this.markers_length; a++) {
            this.markers[a]._encodeRecursive(outs); 
        }
 
    }
 
    public MarkerArray(byte[] data) throws IOException
    {
        this(new LCMDataInputStream(data));
    }
 
    public MarkerArray(DataInput ins) throws IOException
    {
        if (ins.readLong() != LCM_FINGERPRINT)
            throw new IOException("LCM Decode error: bad fingerprint");
 
        _decodeRecursive(ins);
    }
 
    public static visualization_msgs.MarkerArray _decodeRecursiveFactory(DataInput ins) throws IOException
    {
        visualization_msgs.MarkerArray o = new visualization_msgs.MarkerArray();
        o._decodeRecursive(ins);
        return o;
    }
 
    public void _decodeRecursive(DataInput ins) throws IOException
    {
        this.markers_length = ins.readInt();
 
        this.markers = new visualization_msgs.Marker[(int) markers_length];
        for (int a = 0; a < this.markers_length; a++) {
            this.markers[a] = visualization_msgs.Marker._decodeRecursiveFactory(ins);
        }
 
    }
 
    public visualization_msgs.MarkerArray copy()
    {
        visualization_msgs.MarkerArray outobj = new visualization_msgs.MarkerArray();
        outobj.markers_length = this.markers_length;
 
        outobj.markers = new visualization_msgs.Marker[(int) markers_length];
        for (int a = 0; a < this.markers_length; a++) {
            outobj.markers[a] = this.markers[a].copy();
        }
 
        return outobj;
    }
 
}

