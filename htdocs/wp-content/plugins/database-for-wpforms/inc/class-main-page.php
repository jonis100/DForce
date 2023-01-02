<?php
/**
 * WPFormsDB Admin section
 */

if (!defined( 'ABSPATH')) exit;

/**
 * WPFormsDB_Wp_List_Table class will create the page to load the table
 */
class WPFormsDB_Wp_Main_Page
{
    /**
     * Constructor will create the menu item
     */
    public function __construct()
    {
        add_action( 'admin_menu', array($this, 'admin_list_table_page' ) );
    }


    /**
     * Menu item will allow us to load the page to display the table
     */
    public function admin_list_table_page()
    {

		// Fallback: Make sure admin always has access
		$WPFormsDB_cap = ( current_user_can( 'WPFormsDB_access') ) ? 'WPFormsDB_access' : 'manage_options';

        add_menu_page( __( 'WPForms Submissions', 'contact-form-WPFormsDB' ), __( 'WPForms DB', 'contact-form-WPFormsDB' ), 
        $WPFormsDB_cap, 'wp-forms-db-list.php', array($this, 'list_table_page'), 
        'data:image/svg+xml;base64,' . base64_encode('<?xml version="1.0" ?><svg id="Layer_1" style="enable-background:new 0 0 50 50;" version="1.1" viewBox="0 0 50 50" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="Layer_1_1_"><path d="M5,7v42h34v-6h6V1H11v6H5z M37,47H7V9h4h19v7h7v27V47z M32,10.414L35.586,14H32V10.414z M13,3h30v38h-4V14.586L31.414,7H13   V3z"/><rect height="2" width="22" x="11" y="20"/><rect height="2" width="22" x="11" y="26"/><rect height="2" width="22" x="11" y="32"/><rect height="2" width="9" x="11" y="40"/><rect height="2" width="9" x="24" y="40"/><rect height="2" width="8" x="18" y="14"/></g></svg>'));
    }
    /**
     * Display the list table page
     *
     * @return Void
     */
    public function list_table_page()
    {
        if ( ! function_exists('wpforms') ) {

           wp_die( 'Please activate <a href="https://wordpress.org/plugins/wpforms-lite/" target="_blank">WPForms</a> plugin.' );
        }
        wp_enqueue_style( 'wpformsdb-admin-style', plugin_dir_url(dirname(__FILE__)).'admin-style.css' );

        $fid  = empty($_GET['fid']) ? 0 : (int) $_GET['fid'];
        $ufid = empty($_GET['ufid']) ? 0 : (int) $_GET['ufid'];

        if ( !empty($fid) && empty($_GET['ufid']) ) {

            new WPFormsDB_Wp_Sub_Page();
            return;
        }

        if( !empty($ufid) && !empty($fid) ){

            new WPFormsDB_Form_Details();
            return;
        }

        $ListTable = new WPFormsDB_Main_List_Table();
        $ListTable->prepare_items();
        ?>
            <div class="wrap">
                <div id="icon-users" class="icon32"></div>
                <h2><?php _e( 'WPForms List', 'contact-form-WPFormsDB' ); ?></h2>
                <?php $ListTable->display(); ?>
            </div>
        <?php
    }

}
// WP_List_Table is not loaded automatically so we need to load it in our application
if( ! class_exists( 'WP_List_Table' ) ) {
    require_once( ABSPATH . 'wp-admin/includes/class-wp-list-table.php' );
}
/**
 * Create a new table class that will extend the WP_List_Table
 */
class WPFormsDB_Main_List_Table extends WP_List_Table
{

    /**
     * Prepare the items for the table to process
     *
     * @return Void
     */
    public function prepare_items()
    {

        global $wpdb;
        $cfdb        = apply_filters( 'WPFormsDB_database', $wpdb );
        $table_name  = $cfdb->prefix.'wpforms_db';
        $columns     = $this->get_columns();
        $hidden      = $this->get_hidden_columns();
        $data        = $this->table_data();
        $perPage     = 10;
        $currentPage = $this->get_pagenum();
        $count_forms = wp_count_posts('wpforms');
        $totalItems  = $count_forms->publish;


        $this->set_pagination_args( array(
            'total_items' => $totalItems,
            'per_page'    => $perPage
        ) );

        $this->_column_headers = array($columns, $hidden );
        $this->items = $data;
    }
    
    /**
     * Override the parent columns method. Defines the columns to use in your listing table
     *
     * @return Array
     */
    public function get_columns()
    {


        $columns = array(
            'name' => __( 'Name', 'contact-form-WPFormsDB' ),
            'count'=> __( 'Count', 'contact-form-WPFormsDB' )
        );

        return $columns;
    }
    /**
     * Define which columns are hidden
     *
     * @return Array
     */
    public function get_hidden_columns()
    {
        return array();
    }

    /**
     * Get the table data
     *
     * @return Array
     */
    private function table_data()
    {
        global $wpdb;

        $cfdb         = apply_filters( 'WPFormsDB_database', $wpdb );
        $data         = array();
        $table_name   = $cfdb->prefix.'wpforms_db';
        $page         = $this->get_pagenum();
        $page         = $page - 1;
        $start        = $page * 10;

        $args = array(
            'post_type'=> 'wpforms',
            'order'    => 'ASC',
            'posts_per_page' => 10,
            'offset' => $start
        );

        $the_query = new WP_Query( $args );

        while ( $the_query->have_posts() ) : $the_query->the_post();
            $form_post_id = get_the_id();
            $totalItems   = $cfdb->get_var("SELECT COUNT(*) FROM $table_name WHERE form_post_id = $form_post_id");
            $title = get_the_title();
            $link  = "<a class='row-title' href=admin.php?page=wp-forms-db-list.php&fid=$form_post_id>%s</a>";
            $data_value['name']  = sprintf( $link, $title );
            $data_value['count'] = sprintf( $link, $totalItems );
            $data[] = $data_value;
        endwhile;

        return $data;
    }
    /**
     * Define what data to show on each column of the table
     *
     * @param  Array $item        Data
     * @param  String $column_name - Current column name
     *
     * @return Mixed
     */
    public function column_default( $item, $column_name )
    {
        return $item[ $column_name ];

    }

}
