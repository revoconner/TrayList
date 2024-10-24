// todolist.hpp
#pragma once
#include <wx/wx.h>
#include <vector>
#include <string>
#include "trayicon.hpp"
#include <nlohmann/json.hpp>

using json = nlohmann::json;

class TaskEntry : public wxPanel {
public:
    TaskEntry(wxWindow* parent, const wxString& text = "");
    wxString GetText() const;
    void SetText(const wxString& text);

private:
    wxTextCtrl* textCtrl;
    wxButton* deleteButton;
    void OnKeyUp(wxKeyEvent& event);
    void OnEnter(wxCommandEvent& event);
    void OnDelete(wxCommandEvent& event);
};

class MainFrame : public wxFrame {
public:
    MainFrame();
    virtual ~MainFrame();
    
protected:
    void OnClose(wxCloseEvent& event);
    void AddEmptyTask();
    void SaveTasks();
    void LoadTasks();
    void DeleteTask(TaskEntry* task);

private:
    std::vector<TaskEntry*> tasks;
    wxBoxSizer* mainSizer;
    TrayIcon* trayIcon;
    wxPanel* scrolledPanel;
    wxScrolledWindow* scrollWindow;
    
    static const wxString DATA_FILE;
    
    friend class TaskEntry;
    friend class TrayIcon;
};

class TodoApp : public wxApp {
public:
    virtual bool OnInit() override;
};
