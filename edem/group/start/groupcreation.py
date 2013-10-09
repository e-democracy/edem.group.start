# -*- coding: utf-8 -*-
from AccessControl.PermissionRole import rolesForPermissionOn
from gs.group.base.interfaces import IGSGroupMarker


def groupAddedHandler(groupFolder, event):
    assert IGSGroupMarker.providedBy(groupFolder), \
       "groupFolder did not implement IGSGroupFolder!"

    site_root = groupFolder.site_root()
    if site_root.getId() == 'edem':
        # add a participant ID
        groupFolder.manage_addProperty('ptn_coach_id', '', 'string')

        # add a charter, copying it from the template
        assert hasattr(site_root, "Content"), "site_root has no Content folder"
        assert hasattr(site_root.Content, "main"), "Content has no main folder"
        assert hasattr(site_root.Content.main, "charter"), \
            "main has no charter folder"

        charter = getattr(site_root.Content.main, "charter")
        groupFolder.manage_clone(charter, "charter")

    # make sure GroupAdmins can manage the properties of the group
    roles = []
    for set in groupFolder.rolesOfPermission('Manage properties'):
        if set['selected']:
            roles.append(set['name'])

    roles = list(rolesForPermissionOn('Manage properties', groupFolder))
    if 'GroupAdmin' not in roles:
        roles.append('GroupAdmin')
        groupFolder.manage_permission('Manage properties', roles, 1)
    return
