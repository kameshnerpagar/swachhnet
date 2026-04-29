const User = require('../models/User');
const Complaint = require('../models/Complaint');

/**
 * GET /api/central/dashboard
 * Superadmin only
 * Returns system-wide metrics, list of all authorities and breached complaints.
 */
const getCentralDashboard = async (req, res) => {
  try {
    // 1. Fetch all authorities
    const authorities = await User.find({ role: 'admin' }).select('-password').lean();
    
    // 2. Compute system-wide totals and average resolution time
    let totalComplaints = await Complaint.countDocuments();
    let totalResolved = 0;
    let totalResolutionTimeMs = 0;

    const resolvedComplaints = await Complaint.find({ status: 'resolved' }).lean();
    totalResolved = resolvedComplaints.length;

    resolvedComplaints.forEach(c => {
      // updatedAt is roughly the time it was marked resolved
      const resTime = new Date(c.updatedAt).getTime() - new Date(c.createdAt).getTime();
      totalResolutionTimeMs += resTime;
    });

    const avgResTimeMs = totalResolved > 0 ? totalResolutionTimeMs / totalResolved : 0;
    
    // Convert ms to hours
    const avgResolutionHours = avgResTimeMs / (1000 * 60 * 60);

    // 3. Find breached complaints and map them to authorities
    const fortyEightHoursAgo = new Date(Date.now() - 48 * 60 * 60 * 1000);
    const breachedComplaints = await Complaint.find({
      status: { $nin: ['resolved', 'rejected'] },
      createdAt: { $lt: fortyEightHoursAgo }
    }).populate('authorityId', 'name authorityDetails').lean();

    // Map breaches and resolved count per authority
    const authorityMetrics = authorities.map(auth => {
      const authBreaches = breachedComplaints.filter(c => c.authorityId && c.authorityId._id.toString() === auth._id.toString());
      const authResolved = resolvedComplaints.filter(c => c.authorityId && c.authorityId.toString() === auth._id.toString());
      
      return {
        ...auth,
        metrics: {
          activeBreaches: authBreaches.length,
          totalResolved: authResolved.length
        }
      };
    });

    res.json({
      success: true,
      data: {
        systemMetrics: {
          totalWards: authorities.length,
          totalComplaints,
          totalResolved,
          avgResolutionHours: avgResolutionHours.toFixed(1),
          totalBreaches: breachedComplaints.length
        },
        authorities: authorityMetrics,
        breachedComplaints
      }
    });

  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

module.exports = {
  getCentralDashboard
};
