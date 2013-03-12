#------------------------------------------------------------------------------
# Copyright (c) 2013, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from PyQt4.QtCore import QObject

from atom.api import Typed, null

from enaml.widgets.toolkit_object import ProxyToolkitObject


class QtToolkitObject(ProxyToolkitObject):
    """ A Qt implementation of an Enaml ProxyToolkitObject.

    """
    #: A reference to the toolkit widget created by the proxy.
    widget = Typed(QObject)

    #--------------------------------------------------------------------------
    # Initialization API
    #--------------------------------------------------------------------------
    def create_widget(self):
        """ Create the toolkit widget for the proxy object.

        This method is called during the top-down pass, just before the
        'init_widget()' method is called. This method should create the
        toolkit widget and assign it to the 'widget' attribute.

        """
        self.widget = QObject(self.parent_widget())

    def init_widget(self):
        """ Initialize the state of the toolkit widget.

        This method is called during the top-down pass, just after the
        'create_widget()' method is called. This method should init the
        state of the widget. The child widgets will not yet be created.

        """
        pass

    def init_layout(self):
        """ Initialize the layout of the toolkit widget.

        This method is called during the bottom-up pass. This method
        should initialize the layout of the widget. The child widgets
        will be fully initialized and layed out when this is called.

        """
        pass

    #--------------------------------------------------------------------------
    # ProxyToolkitObject API
    #--------------------------------------------------------------------------
    def init_top_down(self):
        """ Initialize the proxy tree for the top-down pass.

        """
        self.create_widget()
        self.init_widget()

    def init_bottom_up(self):
        """ Initialize the proxy tree for the bottom-up pass.

        """
        self.init_layout()

    def destroy(self):
        """ A reimplemented destructor.

        This will destroy the toolkit object provided that the parent
        declaration is no already destroyed. This is so that only the
        top-most toolkit object is destroyed, saving time.

        """
        if self.widget is not null:
            self.widget.setParent(None)
            del self.widget
        super(QtToolkitObject, self).destroy()

    def child_removed(self, child):
        """ Handle the child removed event from the declaration.

        This handler will unparent the child toolkit widget. Subclasses
        which need more control should reimplement this method.

        """
        super(QtToolkitObject, self).child_removed(child)
        if child.widget is not null:
            child.widget.setParent(None)

    #--------------------------------------------------------------------------
    # Public API
    #--------------------------------------------------------------------------
    def parent_widget(self):
        """ Get the parent toolkit widget for this object.

        Returns
        -------
        result : QObject or None
            The toolkit widget declared on the declaration parent, or
            None if there is no such parent.

        """
        d = self.parent()
        if d is not None:
            w = d.widget
            if w is not null:
                return w

    def child_widgets(self):
        """ Get the child toolkit widgets for this object.

        Returns
        -------
        result : iterable of QObject
            The child widgets defined for this object.

        """
        for child in self.children():
            w = child.widget
            if w is not null:
                yield w
