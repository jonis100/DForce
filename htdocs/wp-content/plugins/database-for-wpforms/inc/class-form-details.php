<?php

if (!defined( 'ABSPATH')) exit;

/**
*
*/
class WPFormsDB_Form_Details
{
    private $form_id;
    private $form_post_id;


    public function __construct()
    {
        $this->form_post_id = (int) $_GET['fid'];
        $this->form_id = (int) $_GET['ufid'];

        $this->form_details_page();
    }

    public function form_details_page(){
        global $wpdb;
        $cfdb          = apply_filters( 'WPFormsDB_database', $wpdb );
        $table_name    = $cfdb->prefix.'wpforms_db';
        $upload_dir    = wp_upload_dir();
        $WPFormsDB_dir_url = $upload_dir['baseurl'].'/WPFormsDB_uploads';

        if ( is_numeric($this->form_post_id) && is_numeric($this->form_id) ) {

           $results    = $cfdb->get_results( "SELECT * FROM $table_name WHERE form_post_id = $this->form_post_id AND form_id = $this->form_id LIMIT 1", OBJECT );
        }

        if ( empty($results) ) {
            wp_die( $message = 'Not valid contact form' );
        }
        ?>
        <div class="wrap">
            <div id="welcome-panel" class="cfdb7-panel">
                <div class="cfdb7-panel-content">
                    <div class="welcome-panel-column-container">
                        <?php do_action('WPFormsDB_before_formdetails_title',$this->form_post_id ); ?>
                        <h3><?php echo get_the_title( $this->form_post_id ); ?></h3>
                        <?php do_action('WPFormsDB_after_formdetails_title', $this->form_post_id ); ?>
                        <p></span><?php echo esc_html( $results[0]->form_date ); ?></p>
                        <?php $form_data  = unserialize( $results[0]->form_value );

                        foreach ($form_data as $key => $data):

                            if ( $key == 'WPFormsDB_status' )  continue;

                            if ( strpos($key, 'WPFormsDB_file') !== false ){

                                $key_val = str_replace('WPFormsDB_file', '', $key);
                                $key_val = str_replace('your-', '', $key_val);
                                $key_val = ucfirst( $key_val );
                                echo '<p><b>'.esc_html( $key_val ).'</b>: <a href="'. esc_url( $WPFormsDB_dir_url.'/'.$data ).'">'
                                . esc_html( $data ).'</a></p>';
                            }else{


                                if ( is_array($data) ) {

                                    $key_val = str_replace('your-', '', $key);
                                    $key_val = ucfirst( $key_val );
                                    $arr_str_data =  implode(', ',$data);
                                    $arr_str_data =  nl2br( $arr_str_data );
                                    echo '<p><b>'.esc_html( $key_val ).'</b>: '. esc_html($arr_str_data) .'</p>';

                                }else{

                                    $key_val = str_replace('your-', '', $key);
                                    $key_val = ucfirst( $key_val );
                                    $data    = nl2br( $data );
                                    echo '<p><b>'.esc_html( $key_val ).'</b>: '.esc_html($data).'</p>';
                                }
                            }

                        endforeach;

                        $form_data['WPFormsDB_status'] = 'read';
                        $form_data = serialize( $form_data );
                        $form_id = $results[0]->form_id;

                        $cfdb->query( "UPDATE $table_name SET form_value =
                            '$form_data' WHERE form_id = $form_id"
                        );
                        ?>
                    </div>
                </div>
            </div>
        </div>
        <?php
        do_action('WPFormsDB_after_formdetails', $this->form_post_id );
    }

}
