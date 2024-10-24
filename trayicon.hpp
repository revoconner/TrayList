// trayicon.hpp
#pragma once
#include <wx/wx.h>
#include <wx/taskbar.h>

class MainFrame;  // Forward declaration

class TrayIcon : public wxTaskBarIcon {
public:
    TrayIcon(MainFrame* frame);
    virtual ~TrayIcon() {}

protected:
    virtual wxMenu* CreatePopupMenu() override;
    void OnLeftClick(wxTaskBarIconEvent& event);
    void OnMenuRestore(wxCommandEvent& event);
    void OnMenuExit(wxCommandEvent& event);

private:
    MainFrame* mainFrame;
    wxIcon CreateIcon();
    
    enum {
        ID_MENU_RESTORE = 10001,
        ID_MENU_EXIT
    };

    wxDECLARE_EVENT_TABLE();
};
