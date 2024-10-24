// trayicon.cpp
#include "trayicon.hpp"
#include "todolist.hpp"
#include <wx/bitmap.h>

wxBEGIN_EVENT_TABLE(TrayIcon, wxTaskBarIcon)
    EVT_TASKBAR_LEFT_DOWN(TrayIcon::OnLeftClick)
    EVT_MENU(ID_MENU_RESTORE, TrayIcon::OnMenuRestore)
    EVT_MENU(ID_MENU_EXIT, TrayIcon::OnMenuExit)
wxEND_EVENT_TABLE()

TrayIcon::TrayIcon(MainFrame* frame) : mainFrame(frame) {
    wxIcon icon = CreateIcon();
    SetIcon(icon, "Tray List");
}

wxMenu* TrayIcon::CreatePopupMenu() {
    wxMenu* menu = new wxMenu;
    menu->Append(ID_MENU_RESTORE, "&Open");
    menu->AppendSeparator();
    menu->Append(ID_MENU_EXIT, "E&xit");
    return menu;
}

void TrayIcon::OnLeftClick(wxTaskBarIconEvent& event) {
    mainFrame->Show();
    mainFrame->Raise();
}

void TrayIcon::OnMenuRestore(wxCommandEvent& event) {
    mainFrame->Show();
    mainFrame->Raise();
}

void TrayIcon::OnMenuExit(wxCommandEvent& event) {
    mainFrame->Close(true);
}

wxIcon TrayIcon::CreateIcon() {
    // Load icon from resources or create a simple one
    wxBitmap bmp(16, 16);
    wxMemoryDC dc(bmp);
    dc.SetBackground(*wxBLACK_BRUSH);
    dc.Clear();
    dc.SetBrush(*wxWHITE_BRUSH);
    dc.DrawCircle(8, 8, 7);
    wxIcon icon;
    icon.CopyFromBitmap(bmp);
    return icon;
}
