document.addEventListener('DOMContentLoaded', function() {
    // Navigation
    const sections = document.querySelectorAll('.content-section');
    const navLinks = document.querySelectorAll('.nav-link');
    
    function hideAllSections() {
        sections.forEach(section => {
            section.classList.add('hidden-section');
            section.classList.remove('active-section');
        });
    }
    
    function showSection(sectionId) {
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            hideAllSections();
            targetSection.classList.remove('hidden-section');
            targetSection.classList.add('active-section');
        }
    }
    
    // Show dashboard section by default
    showSection('dashboard-section');
    
    // Set dashboard link as active by default
    const dashboardLink = document.querySelector('[data-section="dashboard-section"]');
    if (dashboardLink) {
        dashboardLink.classList.add('active');
    }
    
    // Handle navigation clicks
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetSectionId = this.getAttribute('data-section');
            
            // Show target section
            showSection(targetSectionId);
            
            // Update active navigation state
            navLinks.forEach(link => link.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Calendar Functionality
    const calendarDaysContainer = document.getElementById('calendar-days');
    const calendarMonthYear = document.getElementById('calendar-month-year');
    const selectedCountElement = document.getElementById('selected-count');
    const selectedDatesElement = document.getElementById('selected-dates');
    const prevMonthButton = document.getElementById('prev-month');
    const nextMonthButton = document.getElementById('next-month');
    const submitButton = document.getElementById('submit-days-btn');

    if (calendarDaysContainer) {
        const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        const today = new Date();
        let currentMonth = today.getMonth();
        let currentYear = today.getFullYear();

        let selectedDates = [];
        const submittedDatesByMonth = {};
        const MAX_SELECTIONS = 5;

        function generateCalendar(month, year) {
            calendarDaysContainer.innerHTML = '';
            calendarMonthYear.textContent = `${monthNames[month]} ${year}`;
            
            const firstDay = new Date(year, month, 1).getDay();
            const daysInMonth = new Date(year, month + 1, 0).getDate();
            const monthKey = `${year}-${month+1}`;
            
            if (!submittedDatesByMonth[monthKey]) {
                submittedDatesByMonth[monthKey] = [];
            }
            
            for (let i = 0; i < firstDay; i++) {
                const emptyDay = document.createElement('div');
                emptyDay.classList.add('calendar-day', 'disabled');
                calendarDaysContainer.appendChild(emptyDay);
            }
            
            const currentDate = new Date();
            currentDate.setHours(0, 0, 0, 0);
            
            for (let day = 1; day <= daysInMonth; day++) {
                const cellDate = new Date(year, month, day);
                const dateString = `${year}-${month+1}-${day}`;
                const dayElement = document.createElement('div');
                dayElement.classList.add('calendar-day');
                dayElement.textContent = day;
                dayElement.dataset.date = dateString;
                
                if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                    dayElement.classList.add('today');
                }
                if (cellDate < currentDate) {
                    dayElement.classList.add('past');
                }
                if (submittedDatesByMonth[monthKey].includes(dateString)) {
                    dayElement.classList.add('submitted');
                } else if (selectedDates.includes(dateString)) {
                    dayElement.classList.add('selected');
                }
                
                dayElement.addEventListener('click', function() {
                    const date = this.dataset.date;
                    if (cellDate < currentDate || this.classList.contains('past') || this.classList.contains('submitted')) {
                        return;
                    }
                    
                    if (this.classList.contains('selected')) {
                        this.classList.remove('selected');
                        const index = selectedDates.indexOf(date);
                        if (index > -1) selectedDates.splice(index, 1);
                    } else {
                        const submittedCount = submittedDatesByMonth[monthKey].length;
                        const selectedForCurrentMonth = selectedDates.filter(d => d.startsWith(`${year}-${month+1}`)).length;
                        
                        if (submittedCount + selectedForCurrentMonth < MAX_SELECTIONS) {
                            this.classList.add('selected');
                            selectedDates.push(date);
                        } else {
                            alert(`You can only select up to ${MAX_SELECTIONS} days off per month.`);
                        }
                    }
                    updateSelectionInfo(monthKey);
                });
                
                calendarDaysContainer.appendChild(dayElement);
            }
        }
        
        function updateSelectionInfo(monthKey) {
            const selectedForCurrentMonth = selectedDates.filter(d => d.startsWith(monthKey));
            const [year, monthNum] = monthKey.split('-');
            const monthName = monthNames[parseInt(monthNum) - 1];
            const monthYearText = `${monthName} ${year}`;
            
            const hasSubmittedDates = submittedDatesByMonth[monthKey] && submittedDatesByMonth[monthKey].length > 0;
            
            if (hasSubmittedDates) {
                selectedCountElement.textContent = submittedDatesByMonth[monthKey].length;
                selectedDatesElement.textContent = `You have already submitted ${submittedDatesByMonth[monthKey].length} day(s) off for ${monthYearText}.`;
                submitButton.style.display = 'none';
            } else {
                selectedCountElement.textContent = selectedForCurrentMonth.length;
                if (selectedForCurrentMonth.length > 0) {
                    const formattedDates = selectedForCurrentMonth.map(dateStr => {
                        const [y, m, d] = dateStr.split('-');
                        const date = new Date(y, m-1, d);
                        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
                    });
                    selectedDatesElement.textContent = `Selected dates: ${formattedDates.join(', ')}`;
                } else {
                    selectedDatesElement.textContent = 'No dates selected yet.';
                }
                submitButton.style.display = 'block';
            }
            submitButton.disabled = selectedForCurrentMonth.length === 0 && !hasSubmittedDates;
        }

        prevMonthButton.addEventListener('click', function() {
            const today = new Date();
            const currentMonthDate = new Date(today.getFullYear(), today.getMonth());
            const targetDate = new Date(currentYear, currentMonth - 1);
            
            if (targetDate >= currentMonthDate) {
                currentMonth--;
                if (currentMonth < 0) {
                    currentMonth = 11;
                    currentYear--;
                }
                generateCalendar(currentMonth, currentYear);
                updateSelectionInfo(`${currentYear}-${currentMonth+1}`);
            }
        });
        
        nextMonthButton.addEventListener('click', function() {
            currentMonth++;
            if (currentMonth > 11) {
                currentMonth = 0;
                currentYear++;
            }
            generateCalendar(currentMonth, currentYear);
            updateSelectionInfo(`${currentYear}-${currentMonth+1}`);
        });
        
        submitButton.addEventListener('click', function() {
            const monthKey = `${currentYear}-${currentMonth+1}`;
            const selectedForCurrentMonth = selectedDates.filter(d => d.startsWith(monthKey));
            
            if (selectedForCurrentMonth.length === 0) {
                alert('Please select at least one day off before submitting.');
                return;
            }
            
            if (!submittedDatesByMonth[monthKey]) {
                submittedDatesByMonth[monthKey] = [];
            }
            
            selectedForCurrentMonth.forEach(date => {
                submittedDatesByMonth[monthKey].push(date);
                const index = selectedDates.indexOf(date);
                if (index > -1) selectedDates.splice(index, 1);
            });
            
            generateCalendar(currentMonth, currentYear);
            updateSelectionInfo(monthKey);
            
            const monthName = monthNames[currentMonth];
            alert(`Successfully submitted ${selectedForCurrentMonth.length} day(s) off for ${monthName} ${currentYear}.`);
        });

        // Initialize calendar
        generateCalendar(currentMonth, currentYear);
        updateSelectionInfo(`${currentYear}-${currentMonth+1}`);
    }

    // Notes Management
    const addNoteBtn = document.getElementById('add-note-btn');
    const notesContainer = document.querySelector('.notes-container');
    
    if (addNoteBtn && notesContainer) {
        addNoteBtn.addEventListener('click', function() {
            const noteTitle = prompt('Enter note title:');
            if (!noteTitle) return;
            
            const noteContent = prompt('Enter note content:');
            if (!noteContent) return;
            
            const today = new Date();
            const noteDate = today.toLocaleDateString('en-US', { 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            });
            
            const noteCard = document.createElement('div');
            noteCard.className = 'note-card';
            noteCard.innerHTML = `
                <div class="note-header">
                    <h3>${noteTitle}</h3>
                    <span class="note-date">${noteDate}</span>
                </div>
                <p class="note-content">${noteContent}</p>
                <div class="note-actions">
                    <button class="btn btn-icon btn-sm edit-note">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                    </button>
                    <button class="btn btn-icon btn-sm delete-note">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </div>
            `;
            
            notesContainer.prepend(noteCard);
            
            // Add event listeners for the new note's buttons
            const editBtn = noteCard.querySelector('.edit-note');
            const deleteBtn = noteCard.querySelector('.delete-note');
            
            editBtn.addEventListener('click', function() {
                const noteTitle = noteCard.querySelector('h3').textContent;
                const noteContent = noteCard.querySelector('.note-content').textContent;
                
                const newTitle = prompt('Edit note title:', noteTitle);
                if (!newTitle) return;
                
                const newContent = prompt('Edit note content:', noteContent);
                if (!newContent) return;
                
                noteCard.querySelector('h3').textContent = newTitle;
                noteCard.querySelector('.note-content').textContent = newContent;
            });
            
            deleteBtn.addEventListener('click', function() {
                if (confirm('Are you sure you want to delete this note?')) {
                    noteCard.remove();
                }
            });
        });
        
        // Add event listeners for existing notes
        document.querySelectorAll('.note-card').forEach(noteCard => {
            const editBtn = noteCard.querySelector('.edit-note');
            const deleteBtn = noteCard.querySelector('.delete-note');
            
            editBtn.addEventListener('click', function() {
                const noteTitle = noteCard.querySelector('h3').textContent;
                const noteContent = noteCard.querySelector('.note-content').textContent;
                
                const newTitle = prompt('Edit note title:', noteTitle);
                if (!newTitle) return;
                
                const newContent = prompt('Edit note content:', noteContent);
                if (!newContent) return;
                
                noteCard.querySelector('h3').textContent = newTitle;
                noteCard.querySelector('.note-content').textContent = newContent;
            });
            
            deleteBtn.addEventListener('click', function() {
                if (confirm('Are you sure you want to delete this note?')) {
                    noteCard.remove();
                }
            });
        });
    }
}); 