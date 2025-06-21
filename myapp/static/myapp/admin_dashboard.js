$(document).ready(function() {
  // Initialize drag and drop functionality
  $(".shift-slot").sortable({
    connectWith: ".shift-slot",
    items: ".shift-assignment",
    placeholder: "shift-placeholder",
    start: function(event, ui) {
      $(ui.item).addClass("dragging");
    },
    stop: function(event, ui) {
      $(ui.item).removeClass("dragging");
      
      // Get employee and day data
      const employee = ui.item.attr("data-employee");
      const day = $(this).attr("data-day");
      
      // Check for conflicts
      checkForConflicts(employee, day);
    }
  });

  
  // Add new shift assignment
  $(".add-shift-btn").on("click", function() {
    const employeeSelect = $("#employeeSelect").val();
    const daySelect = $("#daySelect").val();
    const timeSelect = $("#timeSelect").val();
    
    // Check for conflicts before adding
    if (!checkForConflicts(employeeSelect, daySelect)) {
      // Add shift if no conflicts
      const targetSlot = $(`.shift-slot[data-employee="${employeeSelect}"][data-day="${daySelect}"]`);
      const newShift = $(`<div class="shift-assignment" data-employee="${employeeSelect}" data-shift-time="${timeSelect}">${timeSelect}</div>`);
      targetSlot.append(newShift);
    }
  });
  
  // Handle approve/reject signup buttons
  $(".approve-signup, .reject-signup").on("click", function() {
    const userId = $(this).attr("data-user-id");
    const action = $(this).hasClass("approve-signup") ? "approve" : "reject";
    
    // Set values for confirmation modal
    $("#signupUserId").val(userId);
    $("#signupDecision").val(action);
    $("#signupAction").text(action);
    
    // Show confirmation modal
    $("#signupConfirmModal").removeClass("hidden");
  });
  
  // Handle signup confirmation
  $("#confirmSignupDecision").on("click", function() {
    const userId = $("#signupUserId").val();
    const decision = $("#signupDecision").val();
    
    // Process the decision
    if (decision === "approve") {
      console.log(`Approving signup for user ID: ${userId}`);
      // Add to schedule logic would go here
    } else {
      console.log(`Rejecting signup for user ID: ${userId}`);
    }
    
    // Remove the signup card from the list
    $(`.conflict-card .conflict-actions button[data-user-id="${userId}"]`).closest(".conflict-card").fadeOut(300, function() {
      $(this).remove();
    });
    
    // Close the modal
    $("#signupConfirmModal").addClass("hidden");
  });
  
  // Modal close button functionality
  $(".close-modal").on("click", function() {
    const modalId = $(this).attr("data-modal-target");
    $(`#${modalId}`).addClass("hidden");
  });
  
  // Function to check for conflicts
  function checkForConflicts(employee, day) {
    // Check if employee has conflict on this day
    const conflicts = getEmployeeConflicts(employee, day);
    
    if (conflicts.length > 0) {
      // Show conflict warning modal
      $("#conflictType").text(conflicts[0].type);
      $("#conflictDate").text(conflicts[0].date);
      $("#conflictWarningModal").removeClass("hidden");
      return true;
    }
    
    return false;
  }
  
  // Simulated function to get employee conflicts
  function getEmployeeConflicts(employee, day) {
    // This would typically fetch from server
    // For demo, return simulated conflicts
    const sampleConflicts = [
      { employee: "Sarah Wilson", day: "Wednesday", type: "Time-off request", date: "April 29, 2025", id: "1" },
      { employee: "Alex Johnson", day: "Friday", type: "Medical appointment", date: "May 1, 2025", id: "2" }
    ];
    
    return sampleConflicts.filter(conflict => 
      conflict.employee === employee && conflict.day === day);
  }
  
  // Handle conflict override
  $("#overrideConflict").on("click", function() {
    console.log("Conflict override approved");
    $("#conflictWarningModal").addClass("hidden");
    // Additional logic for tracking overrides would go here
  });
});


$(document).ready(function() {



    // Handle sidebar navigation clicks
    $('.nav-link').click(function(e) {
      e.preventDefault();
      const section = $(this).data('section');
      
      // Hide all content sections
      $('.content-section').removeClass('active');
      
      // Show selected content section
      $(`#${section}-section`).addClass('active');
      
      // Update active nav link
      $('.nav-link').removeClass('active');
      $(this).addClass('active');

      if(section === 'timeoff') {
          loadTimeOffRequests();
      }
  });
  
  // Initialize first section as active
  $('#dashboard-section').addClass('active');
  $('.nav-link[data-section="dashboard"]').addClass('active');

// Tab switching functionality
$('.tab-btn').click(function() {
const tabId = $(this).data('tab');
$('.tab-btn').removeClass('active');
$(this).addClass('active');
$('.tab-content').removeClass('active');
$(`#${tabId}`).addClass('active');
});

// Modal handling
$('[data-modal-target]').click(function() {
const modalId = $(this).data('modal-target');
$(`#${modalId}`).removeClass('hidden');
});

$('.close-modal').click(function() {
const modalId = $(this).data('modal-target');
$(`#${modalId}`).addClass('hidden');
});

// ---------------- Pending signups ----------------

function refreshPendingSignups(){
   const tbody = $('#pending-signups-body');
   if(tbody.length===0) return;
   tbody.html('<tr><td colspan="6">Loading…</td></tr>');
   fetch('/api/signups/')
     .then(r=>r.ok?r.json():Promise.reject('Failed'))
     .then(data=>{
        tbody.empty();
        if(!data.pending || data.pending.length===0){
            tbody.append('<tr><td colspan="6">No pending signups 🎉</td></tr>');
            return;
        }
        data.pending.forEach(u=>{
           const fullName = (u.first_name||u.last_name)? `${u.first_name} ${u.last_name}`.trim():u.username;
           const tr=`<tr data-id="${u.id}">
                <td>${fullName}</td>
                <td>${u.email}</td>
                <td><span class="join-code">—</span></td>
                <td>—</td>
                <td><span class="badge badge-pending">Pending</span></td>
                <td class="actions">
                    <button class="btn btn-success btn-sm approve-btn" data-id="${u.id}">Approve</button>
                    <button class="btn btn-danger btn-sm reject-btn" data-id="${u.id}">Reject</button>
                </td>
           </tr>`;
           tbody.append(tr);
        });
     })
     .catch(err=>{console.error(err); tbody.html('<tr><td colspan="6">Error loading data</td></tr>');});
}

// Approve / Reject actions
$(document).on('click', '.approve-btn, .reject-btn', function(){
   const isApprove=$(this).hasClass('approve-btn');
   const id=$(this).data('id');
   const row=$(this).closest('tr');
   fetch(`/api/signups/${id}/decision/`,{
      method:'POST',
      headers:{'Content-Type':'application/json','X-CSRFToken':getCookie('csrftoken')},
      body: JSON.stringify({decision: isApprove?'approve':'reject'})
   }).then(r=>r.ok?r.json():Promise.reject('Error'))
    .then(()=>{
        row.remove();
        if($('#pending-signups-body tr').length===0){
           $('#pending-signups-body').append('<tr><td colspan="6">No pending signups 🎉</td></tr>');
        }
    }).catch(err=>{alert('Failed: '+err);});
});

// Load signups on page ready and when Dashboard tab shown
refreshPendingSignups();
$('.nav-link[data-section="dashboard"]').click(()=>refreshPendingSignups());

// Shift Management - Drag and Drop functionality
interact('.shift-slot').dropzone({
accept: '.draggable-shift',
overlap: 0.5,
ondropactivate: function(event) {
event.target.classList.add('dragging-over');
},
ondragenter: function(event) {
event.target.classList.add('dragging-over');
},
ondragleave: function(event) {
event.target.classList.remove('dragging-over');
},
ondrop: function(event) {
event.target.classList.remove('dragging-over');
const shift = event.relatedTarget;
const shiftInfo = shift.textContent;

// Check for conflicts before allowing drop
const employee = event.target.dataset.employee;
const day = event.target.dataset.day;

if (checkForConflicts(employee, day, shiftInfo)) {
showConflictWarning(employee, day);
return;
}

// Move the shift to the new slot
event.target.innerHTML = `<div class="draggable-shift" draggable="true">${shiftInfo}</div>`;
event.target.classList.add('assigned');
},
ondropdeactivate: function(event) {
event.target.classList.remove('dragging-over');
}
});

interact('.draggable-shift').draggable({
inertia: true,
modifiers: [
interact.modifiers.restrictRect({
restriction: 'parent',
endOnly: true
})
],
autoScroll: true,
listeners: {
start(event) {
event.target.classList.add('dragging');
},
move(event) {
const target = event.target;
const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

target.style.transform = `translate(${x}px, ${y}px)`;
target.setAttribute('data-x', x);
target.setAttribute('data-y', y);
},
end(event) {
event.target.classList.remove('dragging');
}
}
});

// Assign Shift Modal
$('#confirmAssignShift').click(function() {
const employee = $('#shiftEmployee').val();
const day = $('#shiftDay').val();
const startTime = $('#shiftStartTime').val();
const endTime = $('#shiftEndTime').val();

if (!employee || !day || !startTime || !endTime) {
alert('Please fill all fields');
return;
}

const shiftInfo = `${startTime}-${endTime}`;

// Check for conflicts
if (checkForConflicts(employee, day, shiftInfo)) {
showConflictWarning(employee, day);
return;
}

// Find the target slot and add the shift
const targetSlot = $(`.shift-slot[data-employee="${employee}"][data-day="${day}"]`);
targetSlot.html(`<div class="draggable-shift" draggable="true">${shiftInfo}</div>`);
targetSlot.addClass('assigned');

// Close modal and reset form
$('#assignShiftModal').addClass('hidden');
$('#assignShiftForm')[0].reset();
});

// Conflict Management
$('#confirmAddConflict').click(function() {
const employee1 = $('#conflictEmployee1').val();
const employee2 = $('#conflictEmployee2').val();
const severity = $('#conflictSeverity').val();
const notes = $('#conflictNotes').val();

if (!employee1 || !employee2 || employee1 === employee2) {
alert('Please select two different employees');
return;
}

// In a real app, you would save this to your database
console.log(`Added conflict between ${employee1} and ${employee2} (${severity})`);

// Add to UI
const conflictCard = `
<div class="conflict-card">
<div class="conflict-employees">
    <div class="employee-badge">
        <img src="/api/placeholder/50/50" alt="${employee1}">
        <span>${employee1}</span>
    </div>
    <span class="vs-badge">VS</span>
    <div class="employee-badge">
        <img src="/api/placeholder/50/50" alt="${employee2}">
        <span>${employee2}</span>
    </div>
</div>
<div class="conflict-actions">
    <button class="btn btn-secondary btn-sm edit-conflict" data-conflict-id="new">
        <i class="fas fa-edit"></i> Edit
    </button>
    <button class="btn btn-danger btn-sm remove-conflict" data-conflict-id="new">
        <i class="fas fa-trash"></i> Remove
    </button>
</div>
</div>
`;

$('.conflict-list').append(conflictCard);
$('#addConflictModal').addClass('hidden');
$('#addConflictForm')[0].reset();
});

// Schedule Generator
$('#generateSchedule').click(function() {
// In a real app, this would call your scheduling algorithm
alert('Generating new schedule based on employee availability and conflicts...');

// For demo purposes, we'll just randomly assign some shifts
$('.shift-slot').each(function() {
if (Math.random() > 0.7) {
const times = ['9AM-5PM', '12PM-8PM', '2PM-10PM'];
const randomTime = times[Math.floor(Math.random() * times.length)];
$(this).html(`<div class="draggable-shift" draggable="true">${randomTime}</div>`);
$(this).addClass('assigned');
} else {
$(this).html('');
$(this).removeClass('assigned');
}
});
});

$('#applyGeneratedSchedule').click(function() {
// In a real app, this would save the generated schedule
alert('Generated schedule applied successfully!');
});

// Conflict checking functions
function checkForConflicts(employee, day, shiftInfo) {
// In a real app, this would check your database for conflicts
// For demo purposes, we'll just simulate some conflicts
const conflicts = {
'Alex Johnson': {
'Monday': true,
'Wednesday': true
},
'Sarah Wilson': {
'Friday': true
}
};

return conflicts[employee] && conflicts[employee][day];
}

function showConflictWarning(employee, day) {
alert(`Conflict detected! ${employee} has a scheduling conflict on ${day}.`);
}

// --- Cached employee name -> id mapping ---
let EMPLOYEE_MAP = {};

// Fetch employees once page is ready (for managers)
if (window.location.pathname.includes('admin-dashboard')) {
  fetch('/api/employees/')
    .then(r => r.ok ? r.json() : Promise.reject('Failed to load employees'))
    .then(data => {
      data.employees.forEach(emp => {
        const fullName = emp.first_name || emp.last_name ? `${emp.first_name} ${emp.last_name}`.trim() : emp.username;
        EMPLOYEE_MAP[fullName] = emp.id;
      });

      // After employees are loaded build the schedule grid for the current week
      buildScheduleGrid();
    })
    .catch(err => console.error(err));
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Save shifts
$('#saveShifts').click(function() {
  const weekStartDateObj = (() => { const d=new Date(); const day=d.getDay(); const diff=d.getDate()-day+ (day===0? -6:1); return new Date(d.setDate(diff));})();
  const weekStart = weekStartDateObj.toISOString().split('T')[0];

  const shifts = [];
  $('.shift-slot.assigned').each(function() {
    const employeeName = $(this).data('employee');
    const day = $(this).data('day');
    const time = $(this).find('.draggable-shift').text();

    if (employeeName && day && time) {
      const [start, end] = time.split('-');
      const empId = EMPLOYEE_MAP[employeeName] || null;
      if (!empId) {
        console.warn('Employee id not found for name', employeeName);
        return; // skip
      }
      shifts.push({
        employee_id: empId,
        day: day,
        start: to24(start),
        end: to24(end),
        manual_override: false,
        title: 'Shift'
      });
    }
  });

  if (shifts.length === 0) {
    alert('No shifts to save.');
    return;
  }

  fetch('/api/shifts/bulk-save/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({
      week_start: weekStart,
      shifts: shifts
    })
  })
    .then(r => r.json().then(data => ({status: r.status, data: data})))
    .then(res => {
      if (res.status === 201) {
        alert('Shifts saved successfully!');
      } else {
        alert('Error saving shifts: ' + JSON.stringify(res.data));
      }
    })
    .catch(err => {
      console.error(err);
      alert('Unexpected error saving shifts.');
    });
});

// Conflict removal
$(document).on('click', '.remove-conflict', function() {
if (confirm('Are you sure you want to remove this conflict?')) {
$(this).closest('.conflict-card').remove();
}
});

function to24(timeStr){const m=timeStr.match(/(\d+)(?::(\d+))?(AM|PM)/i);if(!m)return timeStr;let h=parseInt(m[1],10);const min=parseInt(m[2]||'0',10);const ampm=m[3].toUpperCase();if(ampm==='PM'&&h<12)h+=12;if(ampm==='AM'&&h===12)h=0;return `${h.toString().padStart(2,'0')}:${min.toString().padStart(2,'0')}`;}

function loadTimeOffRequests(){
     const tbody = $('#timeoff-table-body');
     tbody.empty();
     fetch('/api/timeoff/')
       .then(r=>r.ok?r.json():Promise.reject('Failed'))
       .then(data=>{
          if(data.requests.length===0){
              tbody.append('<tr><td colspan="5">No pending requests 🎉</td></tr>');
          }
          data.requests.forEach(req=>{
             const row=`<tr data-id="${req.id}">
                <td>${req.user_name}</td>
                <td>${req.start_date} - ${req.end_date}</td>
                <td>${req.reason||''}</td>
                <td><span class="badge badge-pending">Pending</span></td>
                <td>
                   <button class="btn btn-success btn-sm timeoff-approve" data-id="${req.id}">Approve</button>
                   <button class="btn btn-danger btn-sm timeoff-deny" data-id="${req.id}">Deny</button>
                </td>
             </tr>`;
             tbody.append(row);
          });
       })
       .catch(console.error);
  }

$(document).on('click','.timeoff-approve, .timeoff-deny',function(){
      const id=$(this).data('id');
      const decision=$(this).hasClass('timeoff-approve')?'approved':'denied';
      fetch(`/api/timeoff/${id}/decision/`,{
         method:'POST',
         headers:{'Content-Type':'application/json','X-CSRFToken':getCookie('csrftoken')},
         body: JSON.stringify({decision:decision})
      }).then(r=>r.ok?r.json():Promise.reject('Error'))
       .then(()=>{
           $(`tr[data-id='${id}']`).remove();
           if($('#timeoff-table-body tr').length===0){
               $('#timeoff-table-body').append('<tr><td colspan="5">No pending requests 🎉</td></tr>');
           }
       }).catch(err=>{alert('Failed: '+err);});
  });

// Build schedule grid rows dynamically and populate with existing shifts
function buildScheduleGrid() {
  const calendar = $('.shift-calendar');
  const headerRow = calendar.find('.calendar-header');
  // Remove any existing employee rows
  calendar.find('.calendar-row').remove();

  const employeeNames = Object.keys(EMPLOYEE_MAP);
  employeeNames.forEach(name => {
      const row = $('<div/>').addClass('calendar-row');
      row.append(`<div class="employee-name">${name}</div>`);
      const days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];
      days.forEach(day => {
          row.append(`<div class="shift-slot" data-employee="${name}" data-day="${day}"></div>`);
      });
      calendar.append(row);
  });

  // Now load existing shifts for this week and place them
  const weekStartDateObj = (() => { const d=new Date(); const day=d.getDay(); const diff=d.getDate()-day+ (day===0? -6:1); return new Date(d.setDate(diff));})();
  const weekStart = weekStartDateObj.toISOString().split('T')[0];
  const weekEndDate = new Date(weekStartDateObj.getTime() + 6*24*60*60*1000).toISOString().split('T')[0];

  fetch(`/api/shifts/?start=${weekStart}&end=${weekEndDate}`)
    .then(r=>r.ok?r.json():Promise.reject('Failed shift load'))
    .then(data => {
        data.shifts.forEach(s => {
            const empName = Object.keys(EMPLOYEE_MAP).find(key => EMPLOYEE_MAP[key] === s.user_id);
            if (!empName) return;
            const startDt = new Date(s.start_time);
            const endDt = new Date(s.end_time);
            const dayName = startDt.toLocaleDateString('en-US',{weekday:'long'});
            const slot = $(`.shift-slot[data-employee="${empName}"][data-day="${dayName}"]`);
            if(slot.length){
               slot.addClass('assigned');
               const startStr = startDt.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
               const endStr = endDt.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'});
               slot.html(`<div class="draggable-shift" draggable="true">${startStr}-${endStr}</div>`);
            }
        });
    })
    .catch(console.error);
}
});

