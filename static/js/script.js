$(document).ready(function() {
    // Copy to clipboard functionality
    $('#copyButton').click(function() {
        const noteUrl = $('#noteUrl')[0];
        noteUrl.select();
        noteUrl.setSelectionRange(0, 99999); // For mobile devices
        
        navigator.clipboard.writeText(noteUrl.value).then(function() {
            // Show success message
            $('#copyMessage').fadeIn();
            $('#copyButton').addClass('btn-success').removeClass('btn-outline-success');
            $('#copyButton').html('<i class="fas fa-check me-1"></i>Copied!');
            
            // Reset after 2 seconds
            setTimeout(function() {
                $('#copyMessage').fadeOut();
                $('#copyButton').removeClass('btn-success').addClass('btn-outline-success');
                $('#copyButton').html('<i class="fas fa-copy me-1"></i>Copy');
            }, 2000);
        }).catch(function() {
            // Fallback for older browsers
            document.execCommand('copy');
            $('#copyMessage').fadeIn();
        });
    });

    // Copy note content functionality
    $('#copyContent').click(function() {
        const noteContent = $('.note-content pre').text();
        
        navigator.clipboard.writeText(noteContent).then(function() {
            $(this).addClass('btn-success').removeClass('btn-outline-light');
            $(this).html('<i class="fas fa-check me-2"></i>Content Copied!');
            
            setTimeout(() => {
                $(this).removeClass('btn-success').addClass('btn-outline-light');
                $(this).html('<i class="fas fa-copy me-2"></i>Copy Content');
            }, 2000);
        }.bind(this)).catch(function() {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = noteContent;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            
            $(this).addClass('btn-success').removeClass('btn-outline-light');
            $(this).html('<i class="fas fa-check me-2"></i>Content Copied!');
        }.bind(this));
    });

    // Layout switcher functionality
    $('#cardBtn').click(function() {
        switchLayout('card');
        setActiveButton(this);
    });
    
    $('#buttonBtn').click(function() {
        switchLayout('button');
        setActiveButton(this);
    });
    
    $('#listBtn').click(function() {
        switchLayout('list');
        setActiveButton(this);
    });
    
    function switchLayout(layout) {
        // Hide all layouts
        $('#cardLayout, #buttonLayout, #listLayout').addClass('d-none');
        
        // Show selected layout
        if (layout === 'card') {
            $('#cardLayout').removeClass('d-none');
        } else if (layout === 'button') {
            $('#buttonLayout').removeClass('d-none');
        } else if (layout === 'list') {
            $('#listLayout').removeClass('d-none');
        }
        
        // Sync radio button selections
        syncRadioButtons();
    }
    
    function setActiveButton(activeBtn) {
        $('.btn-group .btn').removeClass('active');
        $(activeBtn).addClass('active');
    }
    
    function syncRadioButtons() {
        // Get currently selected value
        const selectedValue = $('input[name="expiration_type"]:checked').val();
        
        // Clear all selections
        $('input[name="expiration_type"]').prop('checked', false);
        
        // Set the same value across all layouts
        $(`input[name="expiration_type"][value="${selectedValue}"]`).prop('checked', true);
    }
    
    // Sync radio buttons when changed
    $('input[name="expiration_type"]').change(function() {
        const selectedValue = $(this).val();
        $('input[name="expiration_type"]').prop('checked', false);
        $(`input[name="expiration_type"][value="${selectedValue}"]`).prop('checked', true);
    });

    // Form validation
    $('#noteForm').submit(function(e) {
        const content = $('#content').val().trim();
        
        if (content.length === 0) {
            e.preventDefault();
            $('#content').addClass('is-invalid');
            $('#content').focus();
            return false;
        }
        
        // Show loading state
        $(this).find('button[type="submit"]').prop('disabled', true)
               .html('<i class="fas fa-spinner fa-spin me-2"></i>Creating...');
    });

    // Remove validation error on input
    $('#content').on('input', function() {
        $(this).removeClass('is-invalid');
    });

    // Add fade-in animation to cards
    $('.card').addClass('fade-in');
    
    // Auto-hide flash messages after 5 seconds
    setTimeout(function() {
        $('.alert-dismissible').alert('close');
    }, 5000);
    
    // Enhanced hover effects for expiration options
    $('.form-check, .expiration-btn, .list-group-item').hover(
        function() {
            $(this).addClass('shadow-sm');
        },
        function() {
            $(this).removeClass('shadow-sm');
        }
    );
    
    // Accessibility improvements
    $('input[type="radio"]').on('focus', function() {
        $(this).closest('.form-check, .expiration-btn, .list-group-item').addClass('outline-primary');
    }).on('blur', function() {
        $(this).closest('.form-check, .expiration-btn, .list-group-item').removeClass('outline-primary');
    });
});