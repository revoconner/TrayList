// todolist.cpp
#include "todolist.hpp"
#include <wx/filename.h>
#include <fstream>

const wxString MainFrame::DATA_FILE = "todo_list.json";

wxIMPLEMENT_APP(TodoApp);

bool TodoApp::OnInit() {
    if (!wxApp::OnInit())
        return false;

    MainFrame* frame = new MainFrame();
    frame->Show(false);
    return true;
}

TaskEntry::TaskEntry(wxWindow* parent, const wxString& text)
    : wxPanel(parent, wxID_ANY)
{
    wxBoxSizer* sizer = new wxBoxSizer(wxHORIZONTAL);

    textCtrl = new wxTextCtrl(this, wxID_ANY, text,
                             wxDefaultPosition, wxDefaultSize,
                             wxTE_PROCESS_ENTER);
    
    deleteButton = new wxButton(this, wxID_ANY, "X",
                               wxDefaultPosition, wxSize(35, -1));
    
    sizer->Add(textCtrl, 1, wxEXPAND | wxALL, 5);
    sizer->Add(deleteButton, 0, wxALL, 5);
    
    SetSizer(sizer);

    // Bind events
    textCtrl->Bind(wxEVT_KEY_UP, &TaskEntry::OnKeyUp, this);
    textCtrl->Bind(wxEVT_TEXT_ENTER, &TaskEntry::OnEnter, this);
    deleteButton->Bind(wxEVT_BUTTON, &TaskEntry::OnDelete, this);
}

void TaskEntry::OnKeyUp(wxKeyEvent& event) {
    // Save on every key press except Enter
    if (event.GetKeyCode() != WXK_RETURN) {
        MainFrame* frame = static_cast<MainFrame*>(GetGrandParent()->GetParent());
        frame->SaveTasks();
    }
    event.Skip();
}

void TaskEntry::OnEnter(wxCommandEvent& event) {
    if (!textCtrl->IsEmpty()) {
        MainFrame* frame = static_cast<MainFrame*>(GetGrandParent()->GetParent());
        frame->AddEmptyTask();
        frame->SaveTasks();
    }
}

void TaskEntry::OnDelete(wxCommandEvent& event) {
    MainFrame* frame = static_cast<MainFrame*>(GetGrandParent()->GetParent());
    frame->DeleteTask(this);
    frame->SaveTasks();
}

wxString TaskEntry::GetText() const {
    return textCtrl->GetValue();
}

void TaskEntry::SetText(const wxString& text) {
    textCtrl->SetValue(text);
}

MainFrame::MainFrame()
    : wxFrame(nullptr, wxID_ANY, "Tray List", 
              wxDefaultPosition, wxSize(500, 600))
{
    SetBackgroundColour(*wxBLACK);
    
    mainSizer = new wxBoxSizer(wxVERTICAL);
    
    // Create scrolled window for tasks
    scrollWindow = new wxScrolledWindow(this, wxID_ANY);
    scrollWindow->SetScrollRate(0, 5);
    
    scrolledPanel = new wxPanel(scrollWindow);
    wxBoxSizer* scrollSizer = new wxBoxSizer(wxVERTICAL);
    scrolledPanel->SetSizer(scrollSizer);
    
    // Load existing tasks
    LoadTasks();
    
    // Add initial empty task if none exist
    if (tasks.empty()) {
        AddEmptyTask();
    }
    
    scrollWindow->SetSizer(new wxBoxSizer(wxVERTICAL));
    scrollWindow->GetSizer()->Add(scrolledPanel, 1, wxEXPAND);
    
    mainSizer->Add(scrollWindow, 1, wxEXPAND);
    SetSizer(mainSizer);
    
    // Create tray icon
    trayIcon = new TrayIcon(this);
    
    // Bind events
    Bind(wxEVT_CLOSE_WINDOW, &MainFrame::OnClose, this);
}

MainFrame::~MainFrame() {
    delete trayIcon;
}

void MainFrame::OnClose(wxCloseEvent& event) {
    if (event.CanVeto()) {
        Hide();
        event.Veto();
    } else {
        SaveTasks();
        Destroy();
    }
}

void MainFrame::AddEmptyTask() {
    TaskEntry* task = new TaskEntry(scrolledPanel);
    tasks.push_back(task);
    scrolledPanel->GetSizer()->Add(task, 0, wxEXPAND | wxALL, 5);
    scrolledPanel->Layout();
    scrollWindow->FitInside();
}

void MainFrame::DeleteTask(TaskEntry* task) {
    auto it = std::find(tasks.begin(), tasks.end(), task);
    if (it != tasks.end()) {
        tasks.erase(it);
        task->Destroy();
        scrolledPanel->Layout();
        scrollWindow->FitInside();
    }
}

void MainFrame::SaveTasks() {
    json j = json::array();
    for (const auto& task : tasks) {
        std::string text = task->GetText().ToStdString();
        if (!text.empty()) {
            j.push_back(text);
        }
    }
    
    std::ofstream file(DATA_FILE.ToStdString());
    file << j.dump(4);
}

void MainFrame::LoadTasks() {
    if (wxFileName::FileExists(DATA_FILE)) {
        std::ifstream file(DATA_FILE.ToStdString());
        json j;
        file >> j;
        
        for (const auto& text : j) {
            TaskEntry* task = new TaskEntry(scrolledPanel, 
                                          wxString::FromUTF8(text.get<std::string>()));
            tasks.push_back(task);
            scrolledPanel->GetSizer()->Add(task, 0, wxEXPAND | wxALL, 5);
        }
        scrolledPanel->Layout();
        scrollWindow->FitInside();
    }
}
