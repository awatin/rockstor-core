"""
Copyright (c) 2012-2013 RockStor, Inc. <http://rockstor.com>
This file is part of RockStor.

RockStor is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation; either version 2 of the License,
or (at your option) any later version.

RockStor is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from rest_framework import serializers
from storageadmin.models import (Disk, Pool, Share, Snapshot, NFSExport,
                                 SambaShare, IscsiTarget, Appliance,
                                 SupportCase, DashboardConfig,
                                 NetworkInterface, User, PoolScrub, Setup,
                                 NFSExportGroup, SFTP, Plugin, InstalledPlugin,
                                 AdvancedNFSExport, OauthApp, NetatalkShare,
                                 Group, PoolBalance, SambaCustomConfig,
                                 TLSCertificate, RockOn, DVolume, DPort,
                                 DCustomConfig, SMARTAttribute,
                                 SMARTCapability, SMARTInfo, SMARTErrorLog,
                                 SMARTErrorLogSummary, SMARTTestLog,
                                 SMARTTestLogDetail, SMARTIdentity)
from django.contrib.auth.models import User as DjangoUser


class DiskInfoSerializer(serializers.ModelSerializer):
    pool_name = serializers.CharField(source='pool_name')

    class Meta:
        model = Disk


class PoolInfoSerializer(serializers.ModelSerializer):
    disks = DiskInfoSerializer(source='disk_set')
    free = serializers.IntegerField(source='cur_free')
    reclaimable = serializers.IntegerField(source='cur_reclaimable')

    class Meta:
        model = Pool


class SnapshotSerializer(serializers.ModelSerializer):
    r_usage = serializers.IntegerField(source='cur_rusage')
    e_usage = serializers.IntegerField(source='cur_eusage')

    class Meta:
        model = Snapshot


class NFSExportSerializer(serializers.ModelSerializer):
    share = serializers.CharField(source='share_name')

    class Meta:
        model = NFSExport


class NFSExportGroupSerializer(serializers.ModelSerializer):
    exports = NFSExportSerializer(source='nfsexport_set')

    class Meta:
        model = NFSExportGroup


class AdvancedNFSExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancedNFSExport


class SUserSerializer(serializers.ModelSerializer):
    groupname = serializers.CharField(source='groupname')

    class Meta:
        model = User
        fields = ('username', 'uid', 'gid', 'user', 'public_key', 'admin',
                  'group', 'groupname', 'shell',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group


class UserSerializer(serializers.ModelSerializer):
    suser = SUserSerializer(source='suser')

    class Meta:
        model = DjangoUser
        fields = ('username', 'is_active', 'suser')


class SambaCustomConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = SambaCustomConfig


class SambaShareSerializer(serializers.ModelSerializer):
    share = serializers.CharField(source='share_name')
    admin_users = SUserSerializer(source='admin_users')
    custom_config = SambaCustomConfigSerializer(source='sambacustomconfig_set')

    class Meta:
        model = SambaShare


class IscsiSerializer(serializers.ModelSerializer):

    class Meta:
        model = IscsiTarget


class ShareSerializer(serializers.ModelSerializer):
    snapshots = SnapshotSerializer(source='snapshot_set')
    pool = PoolInfoSerializer(source='pool')
    nfs_exports = NFSExportSerializer(source='nfsexport_set')
    r_usage = serializers.IntegerField(source='cur_rusage')
    e_usage = serializers.IntegerField(source='cur_eusage')

    class Meta:
        model = Share


class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportCase


class DashboardConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardConfig


class NetworkInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkInterface


class PoolScrubSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoolScrub


class PoolBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoolBalance


class SetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setup


class SFTPSerializer(serializers.ModelSerializer):
    share = serializers.CharField(source='share_name')

    class Meta:
        model = SFTP


class PluginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plugin


class InstalledPluginSerializer(serializers.ModelSerializer):
    plugin_meta = PluginSerializer(source='plugin_meta')

    class Meta:
        model = InstalledPlugin


class OauthAppSerializer(serializers.ModelSerializer):
    client_id = serializers.CharField(source='client_id')
    client_secret = serializers.CharField(source='client_secret')

    class Meta:
        model = OauthApp


class NetatalkShareSerializer(serializers.ModelSerializer):
    share = serializers.CharField(source='share_name')

    class Meta:
        model = NetatalkShare


class TLSCertificateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TLSCertificate


class RockOnSerializer(serializers.ModelSerializer):

    class Meta:
        model = RockOn


class RockOnVolumeSerializer(serializers.ModelSerializer):
    share_name = serializers.CharField(source='share_name')

    class Meta:
        model = DVolume


class RockOnPortSerializer(serializers.ModelSerializer):

    class Meta:
        model = DPort


class RockOnCustomConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = DCustomConfig

class SMARTCapabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = SMARTCapability

class SMARTAttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = SMARTAttribute

class SMARTErrorLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = SMARTErrorLog

class SMARTErrorLogSummarySerializer(serializers.ModelSerializer):

    class Meta:
        model = SMARTErrorLogSummary

class SMARTTestLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = SMARTTestLog

class SMARTTestLogDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SMARTTestLogDetail

class SMARTIdentitySerializer(serializers.ModelSerializer):

    class Meta:
        model = SMARTIdentity

class SMARTInfoSerializer(serializers.ModelSerializer):
    capabilities = SMARTCapabilitySerializer(source='capabilities')
    attributes = SMARTAttributeSerializer(source='attributes')
    errorlog = SMARTErrorLogSerializer(source='errorlog')
    errorlogsummary = SMARTErrorLogSummarySerializer(source='errorlogsummary')
    identity = SMARTIdentitySerializer(source='identity')
    testlog = SMARTTestLogSerializer(source='testlog')
    testlogdetail = SMARTTestLogDetailSerializer(source='testlogdetail')

    class Meta:
        model = SMARTInfo
